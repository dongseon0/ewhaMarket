from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import sys
import math

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()


# 메인
@application.route("/")
def hello():
    data = DB.get_items()
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))

    isAuction = {}
    for item_key in data.keys():
        is_auction_status = DB.get_is_auction_status(item_key)
        isAuction[item_key] = is_auction_status

    filtered_data = {}
    for item_key, auction_status in isAuction.items():
        if auction_status == False:  # False인 경우에만 추가
            filtered_data[item_key] = data[item_key]

    filtered_auction_data = {}
    for item_key, auction_status in isAuction.items():
        if auction_status == True:  # True인 경우에만 추가
            filtered_auction_data[item_key] = data[item_key]

    locals()['data_{}'.format(0)] = dict(list(filtered_data.items())[0:5])
    locals()['auction_data_{}'.format(0)] = dict(list(filtered_auction_data.items())[0:5])

    item_counts = len(filtered_data)
    auction_item_counts = len(filtered_auction_data)
    empty_cells = 5 - item_counts if 5 > item_counts else 0
    auction_empty_cells = 5 - auction_item_counts if 5 > auction_item_counts else 0

    return render_template(
        "main_page.html",
        data=filtered_data.items(),
        row1=locals()['data_0'].items(),
        row1_auction=locals()['auction_data_0'].items(),
        empty_cells=empty_cells,
        auction_empty_cells=auction_empty_cells
    )


# 상품
# 전체 상품 리스트
@application.route("/product_list")
def view_product_list():
    # html에 페이지 인덱스 클릭할 때마다 get으로 받아옴
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    per_page = 16  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)  # 페이지 인덱스로 start_idx, end_idx 생성
    if category == "all":
        data = DB.get_items()  # read the table
    else:
        data = DB.get_items_bycategory(category)
    # data = DB.get_items()   read the table
    # 최근 등록된 상품 순으로 보이게
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
    item_counts = len(data)
    """
    if data is None:
        data = {}  # 또는 [] 등 비어있는 데이터로 초기화
        item_counts = 0
    else:
        item_counts = len(data)
    """
    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])
    # 한 페이지에 start_idx, end_idx 만큼 읽어오기
    # data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:(i+1)*per_row])

    empty_cells = per_row - item_counts % per_row if per_row > item_counts % per_page else 0

    isAuction = {}
    for item_key in data.keys():
        is_auction_status = DB.get_is_auction_status(item_key)
        isAuction[item_key] = is_auction_status

    return render_template(
        "product_list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        row4=locals()['data_3'].items(),
        limit=per_page,
        page=page,  # 현재 페이지 인덱스
        page_count=int(math.ceil(item_counts/per_page)),  # 페이지 개수
        total=item_counts,
        category=category,
        empty_cells=empty_cells,
        isAuction=isAuction
    )


# 경매 상품 리스트
@application.route("/auction_list")
def view_auction_list():
    # html에 페이지 인덱스 클릭할 때마다 get으로 받아옴
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    per_page = 16  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)  # 페이지 인덱스로 start_idx, end_idx 생성

    if category == "all":
        data = DB.get_items()  # read the table
    else:
        data = DB.get_items_bycategory(category)

    # 최근 등록된 상품 순으로 정렬
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))

    isAuction = {}
    for item_key in data.keys():
        is_auction_status = DB.get_is_auction_status(item_key)
        isAuction[item_key] = is_auction_status

    # TRUE인 상품만 필터링하여 새로운 딕셔너리에 추가
    filtered_data = {}
    for item_key, auction_status in isAuction.items():
        if auction_status == True:  # TRUE인 경우에만 추가
            filtered_data[item_key] = data[item_key]

    item_counts = len(filtered_data)  # 필터링된 상품 개수 업데이트

    # 페이지에 맞게 데이터 슬라이싱
    if item_counts <= per_page:
        filtered_data = dict(list(filtered_data.items())[:item_counts])
    else:
        filtered_data = dict(list(filtered_data.items())[start_idx:end_idx])

    # 각 행 별 데이터 생성
    tot_count = len(filtered_data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(filtered_data.items())[i * per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(filtered_data.items())[i * per_row:(i + 1) * per_row])

    empty_cells = per_row - item_counts % per_row if per_row > item_counts % per_page else 0

    return render_template(
        "auction_list.html",
        datas=filtered_data.items(),  # 필터링된 데이터 전달
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        row4=locals()['data_3'].items(),
        limit=per_page,
        page=page,  # 현재 페이지 인덱스
        page_count=int(math.ceil(item_counts / per_page)),  # 페이지 개수
        total=item_counts,
        category=category,
        empty_cells=empty_cells,
        isAuction=isAuction
    )


# 일반 상품 리스트
@application.route("/list")
def view_list():
    # html에 페이지 인덱스 클릭할 때마다 get으로 받아옴
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    per_page = 16  # item count to display per page
    per_row = 4  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)  # 페이지 인덱스로 start_idx, end_idx 생성

    if category == "all":
        data = DB.get_items()  # read the table
    else:
        data = DB.get_items_bycategory(category)

    # 최근 등록된 상품 순으로 정렬
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))

    isAuction = {}
    for item_key in data.keys():
        is_auction_status = DB.get_is_auction_status(item_key)
        isAuction[item_key] = is_auction_status

    # TRUE인 상품만 필터링하여 새로운 딕셔너리에 추가
    filtered_data = {}
    for item_key, auction_status in isAuction.items():
        if auction_status == False:  # False인 경우에만 추가
            filtered_data[item_key] = data[item_key]

    item_counts = len(filtered_data)  # 필터링된 상품 개수 업데이트

    # 페이지에 맞게 데이터 슬라이싱
    if item_counts <= per_page:
        filtered_data = dict(list(filtered_data.items())[:item_counts])
    else:
        filtered_data = dict(list(filtered_data.items())[start_idx:end_idx])

    # 각 행 별 데이터 생성
    tot_count = len(filtered_data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(filtered_data.items())[i * per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(filtered_data.items())[i * per_row:(i + 1) * per_row])

    empty_cells = per_row - item_counts % per_row if per_row > item_counts % per_page else 0

    return render_template(
        "list.html",
        datas=filtered_data.items(),  # 필터링된 데이터 전달
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        row4=locals()['data_3'].items(),
        limit=per_page,
        page=page,  # 현재 페이지 인덱스
        page_count=int(math.ceil(item_counts / per_page)),  # 페이지 개수
        total=item_counts,
        category=category,
        empty_cells=empty_cells,
        isAuction=isAuction
    )


# 상품 등록하기
@application.route("/reg_item")
def reg_item():
    if session.get('id') is None:
        flash("로그인 후 상품을 등록해주세요.")
        return render_template("login.html")
    else:
        return render_template("reg_item.html")


@application.route("/submit_item_post", methods=['POST'])
def submit_item_post():
    image_file = request.files["file"]
    image_file.save("static/images/items/{}".format(image_file.filename))
    data = request.form
    data_key = DB.insert_item(data, image_file.filename, session.get('id'))
    return redirect(url_for('view_details_of_item', key=data_key))


@application.route("/details_of_item/<key>/")
def view_details_of_item(key):
    data = DB.get_item_bykey(str(key))
    profile_image_path = DB.get_profile_image_path_byid(data.get('sellerId'))
    if data.get('isAuction') == True:
        return render_template("details_of_auction_item.html", key=key, data=data, profile_image_path=profile_image_path, winner=data.get('winner'))
    else:
        return render_template("details_of_item.html", key=key, data=data, profile_image_path=profile_image_path)


@application.route('/auction/<key>/<sellerId>/<selectRisingPrice>/', methods=['POST'])
def set_auction(key, sellerId, selectRisingPrice):
    if session.get('id') is None:
        return jsonify({'msg': '로그인 후 입찰할 수 있습니다.'})
    elif sellerId == session.get('id'):
        return jsonify({'msg': '내 상품에는 입찰할 수 없습니다.'})
    else:
        DB.set_auction(key, selectRisingPrice, session.get('id'))
        return jsonify({'msg': '입찰 완료했습니다!'})


@application.route("/delete_item/<key>/<sellerId>/")
def delete_item(key, sellerId):
    DB.delete_item_bykey(key, sellerId)
    return redirect(url_for('view_product_list'))


# 리뷰
# 리뷰 작성하기
@application.route("/reg_review/<id>/")
def reg_review(id):
    if session.get('id') is None:
        return render_template("login.html")
    elif id == session.get('id'):
        return redirect(url_for('view_user_reviews', id=id))
    else:
        return render_template("reg_review.html", sellerId=id)


# 리뷰 등록하기
@application.route("/submit_review_post", methods=['POST'])
def submit_review_post():
    data = request.form
    image_file = request.files["file"]
    if image_file:
        image_file.save("static/images/reviews/{}".format(image_file.filename))

    sellerId = data.get('sellerId')
    review_key = DB.reg_review(
        data, image_file.filename, buyerId=data.get('buyerId'), sellerId=sellerId)
    return redirect(url_for('view_details_of_review', key=review_key, sellerId=sellerId))


# 리뷰 상세보기
@application.route("/details_of_review/<sellerId>/<key>/")
def view_details_of_review(key, sellerId):
    data = DB.get_review_bykey(key, sellerId)
    good = DB.get_review_good_bykey(key, sellerId)
    bad = DB.get_review_bad_bykey(key, sellerId)
    profile_image_path = DB.get_profile_image_path_byid(data.get('buyerId'))
    return render_template("details_of_review.html", data=data, key=key, sellerId=sellerId, good=good, bad=bad, profile_image_path=profile_image_path)


# 리뷰 삭제하기
@application.route("/delete_review/<key>/<sellerId>/")
def delete_review(key, sellerId):
    DB.delete_review_bykey(key, sellerId)
    return redirect(url_for('view_user_reviews', id=sellerId))


# 리뷰 상세보기에서 하트 불러오기
@application.route('/show_review_heart/<sellerId>/<key>/', methods=['GET'])
def show_review_heart(key, sellerId):
    heart = DB.get_review_heart_bykey(session['id'], key, sellerId)
    return jsonify({'heart': heart})


# 리뷰 상세보기에서 하트 업데이트하기
@application.route('/update_review_heart/<sellerId>/<key>/<heart>/', methods=['POST'])
def update_review_heart(key, sellerId, heart):
    msg = DB.update_review_heart(session['id'], key, sellerId, heart)
    return jsonify({'msg': msg})


# 유저 리뷰 목록
@application.route("/user_reviews/<id>/")
def view_user_reviews(id):
    page = request.args.get("page", 0, type=int)
    per_page = 5  # item count to display per page
    per_row = 1  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)  # 페이지 인덱스로 start_idx, end_idx 생성
    data = DB.get_reviews(id)  # read the table
    if not data:
        data = {}
        item_counts = 0
    else:
        item_counts = len(data)

    # 한 페이지에 start_idx, end_idx 만큼 읽어오기
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "user_reviews.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        row4=locals()['data_3'].items(),
        row5=locals()['data_4'].items(),
        limit=per_page,
        page=page,  # 현재 페이지 인덱스
        page_count=int((item_counts/per_page) + 1),  # 페이지 개수
        total=item_counts,
        id=id
    )


# 로그인
@application.route("/login")
def login():
    return render_template("login.html")


# 로그인 버튼 클릭
@application.route("/login_confirm", methods=['POST'])
def login_user():
    id = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id, pw_hash):
        session['id'] = id
        return redirect(url_for('hello'))
    else:
        flash("아이디 혹은 비밀번호가 틀렸습니다.")
        return render_template("login.html")


# 로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))


# 회원가입
@application.route("/signup")
def signup():
    return render_template("signup.html")


# 회원가입 버튼 클릭
@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("이미 존재하는 아이디입니다.")
        return render_template("signup.html")


# 마이페이지_내 상점
@application.route("/my_page/<id>/")
def my_page(id):
    page = request.args.get("page", 0, type=int)
    per_page = 6  # 페이지당 표시할 아이템 수
    per_row = 3  # 한 행당 표시할 아이템 수
    row_count = int(per_page / per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    data = DB.get_lists(id)  # 테이블 읽기
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
    if not data:
        data = {}
        item_counts = 0
    else:
        item_counts = len(data)

    # 페이지 당 start_idx부터 end_idx까지 읽기
    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:(i+1)*per_row])

    empty_cells = per_row - item_counts if per_row > item_counts else 0

    isAuction = {}
    for item_key in data.keys():
        is_auction_status = DB.get_is_auction_status(item_key)
        isAuction[item_key] = is_auction_status

    return render_template(
        "my_page.html",
        per_row=per_row,
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts / per_page) + 1),
        total=item_counts,
        id=id,
        empty_cells=empty_cells,
        isAuction=isAuction
    )


# 마이페이지_내 리뷰
@application.route("/my_reviews/<id>/")
def my_reviews(id):
    page = request.args.get("page", 0, type=int)
    per_page = 5  # item count to display per page
    per_row = 1  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)  # 페이지 인덱스로 start_idx, end_idx 생성
    data = DB.get_reviews(id)  # read the table
    if not data:
        data = {}
        item_counts = 0
    else:
        item_counts = len(data)

    # 한 페이지에 start_idx, end_idx 만큼 읽어오기
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "my_reviews.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        row4=locals()['data_3'].items(),
        row5=locals()['data_4'].items(),
        limit=per_page,
        page=page,  # 현재 페이지 인덱스
        page_count=int((item_counts/per_page) + 1),  # 페이지 개수
        total=item_counts,
        id=id
    )


# 마이페이지_찜
@application.route("/my_wish/<id>/")
def my_wish(id):
    page = request.args.get("page", 0, type=int)
    per_page = 6  # 페이지당 표시할 아이템 수
    per_row = 3  # 한 행당 표시할 아이템 수
    row_count = int(per_page / per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    data = DB.get_items_byheart(id)  # 테이블 읽기
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
    if not data:
        data = {}
        item_counts = 0
    else:
        item_counts = len(data)

    # 페이지 당 start_idx부터 end_idx까지 읽기
    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:(i+1)*per_row])

    empty_cells = per_row - item_counts if per_row > item_counts else 0

    isAuction = {}
    for item_key in data.keys():
        is_auction_status = DB.get_is_auction_status(item_key)
        isAuction[item_key] = is_auction_status

    return render_template(
        "my_wish.html",
        per_row=per_row,
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts / per_page) + 1),
        total=item_counts,
        id=id,
        empty_cells=empty_cells,
        isAuction=isAuction
    )


# 마이페이지_개인정보
@application.route("/my_info/<id>/")
def my_infol(id):
    data = DB.get_user_info(id)
    profile = DB.get_profile_image_path_byid(id)
    return render_template("my_info.html", id=id, data=data, profile=profile)


# 마이페이지_개인정보 수정
@application.route("/change_my_info", methods=['POST'])
def change_my_info():
    id = session['id']
    image_file = request.files["file"]
    image_file.save("static/images/profiles/{}".format(image_file.filename))
    DB.set_profile_image(id, image_file.filename)
    data = DB.get_user_info(id)
    profile = DB.get_profile_image_path_byid(id)
    return render_template("my_info.html", id=id, data=data, profile=profile)


# 그외
@application.route("/dynamicurl/<varible_name>/")
def DynamicUrl(variable_name):
    return str(variable_name)


# 로그인 했는지 확인하는 기능
@application.route('/check_login_status/', methods=['GET'])
def check_login_status():
    is_logged_in = 'id' in session
    return jsonify({'is_logged_in': is_logged_in})


# 찜하기 했었는지 조회
@application.route('/show_heart/<key>/', methods=['GET'])
def show_heart(key):
    my_heart = DB.get_heart_bykey(session.get('id'), key)
    return jsonify({'my_heart': my_heart})


# 찜하기 기능
@application.route('/like/<key>/', methods=['POST'])
def like(key):
    try:
        user_id = session['id']
        DB.update_heart(user_id, 'Y', key)
        return jsonify({'msg': '찜하기를 눌렀어요.'})

    except KeyError:
        response_data = {'error': '로그인이 필요합니다.',
                         'redirect_url': url_for('login')}
        return jsonify(response_data), 401


# 찜하기 취소
@application.route('/unlike/<key>/', methods=['POST'])
def unlike(key):
    try:
        user_id = session['id']
        DB.update_heart(user_id, 'N', key)
        return jsonify({'msg': '찜하기를 취소했어요.'})

    except KeyError:
        response_data = {'error': '로그인이 필요합니다.',
                         'redirect_url': url_for('login')}
        return jsonify(response_data), 401


# 유저 판매내역
@application.route("/user_list/<id>/")
def view_user_list(id):
    page = request.args.get("page", 0, type=int)
    per_page = 6  # 페이지당 표시할 아이템 수
    per_row = 3  # 한 행당 표시할 아이템 수
    row_count = int(per_page / per_row)
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    data = DB.get_lists(id)  # 테이블 읽기
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
    if not data:
        data = {}
        item_counts = 0
    else:
        item_counts = len(data)

    # 페이지 당 start_idx부터 end_idx까지 읽기
    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else:
        data = dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)
    for i in range(row_count):  # last row
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(
                list(data.items())[i*per_row:(i+1)*per_row])

    empty_cells = per_row - item_counts if per_row > item_counts else 0

    isAuction = {}
    for item_key in data.keys():
        is_auction_status = DB.get_is_auction_status(item_key)
        isAuction[item_key] = is_auction_status

    return render_template(
        "user_list.html",
        per_row=per_row,
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts / per_page) + 1),
        total=item_counts,
        id=id,
        empty_cells=empty_cells,
        isAuction=isAuction
    )


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
