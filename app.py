from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()


# 메인
@application.route("/")
def hello():
    # return render_template("index.html")
    return redirect(url_for('view_product_list'))


# 상품
@application.route("/product_list")
def view_product_list():
    # html에 페이지 인덱스 클릭할 때마다 get으로 받아옴
    page = request.args.get("page", 0, type=int)
    per_page = 12  # item count to display per page
    per_row = 3  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)  # 페이지 인덱스로 start_idx, end_idx 생성
    data = DB.get_items()  # read the table
    if data is None:
        data = {}  # 또는 [] 등 비어있는 데이터로 초기화
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
        "product_list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        row3=locals()['data_2'].items(),
        row4=locals()['data_3'].items(),
        limit=per_page,
        page=page,  # 현재 페이지 인덱스
        page_count=int((item_counts/per_page) + 1),  # 페이지 개수
        total=item_counts
    )


@application.route("/auction_list")
def view_auction_list():
    return render_template("auction_list.html")


@application.route("/list")
def view_list():
    return render_template("list.html")


@application.route("/reg_item")
def reg_item():
    if session.get('id') is None:
        flash("로그인 후 상품을 등록해주세요.")
        return render_template("login.html")
    else:
        return render_template("reg_item.html")


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/items/{}".format(image_file.filename))
    data = request.form
    data_key = DB.insert_item(data, image_file.filename, id=session.get('id'))
    return redirect(url_for('view_details_of_item', key=data_key))


@application.route("/view_detail/<key>/")
def view_details_of_item(key):
    # get_item_byname 상품 이름으로 데이터 가져오는 함수 생성
    data = DB.get_item_bykey(str(key))
    return render_template("details_of_item.html", key=key, data=data)


# 리뷰
@application.route("/reg_review/<id>/")
def reg_review_init(id):
    if session.get('id') is None:
        flash("로그인 후 리뷰를 작성해주세요.")
        return render_template("login.html")
    else:
        return render_template("reg_review.html", buyerId=session.get('id'), sellerId=id)


@application.route("/reg_review", methods=['POST'])
def reg_review():
    image_file = request.files["file"]
    image_file.save("static/images/reviews/{}".format(image_file.filename))
    data = request.form
    sellerId = data.get('sellerId')
    review_key = DB.reg_review(
        data, image_file.filename, buyerId=data.get('buyerId'), sellerId=sellerId)
    return redirect(url_for('view_details_of_review', key=review_key, sellerId=sellerId))


@application.route("/details_of_review/<sellerId>/<key>/")
def view_details_of_review(key, sellerId):
    data = DB.get_review_bykey(key, sellerId)
    return render_template("details_of_review.html", data=data)


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


@application.route("/user_list/<id>/")
def view_user_list(id):
    return render_template("user_list.html", id=id)


# 로그인
@application.route("/login")
def login():
    return render_template("login.html")


@application.route("/login_confirm", methods=['POST'])
def login_user():
    id = request.form['id']
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id, pw_hash):
        session['id'] = id
        return redirect(url_for('hello'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")


@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))


@application.route("/signup")
def signup():
    return render_template("signup.html")


@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")


# 마이페이지
@application.route("/my_page/<id>/")
def mypage(id):
    return render_template("my_page.html", id=id)


@application.route("/my_reviews/<id>/")
def myreview(id):
    return render_template("my_reviews.html", id=id)


@application.route("/my_wish/<id>/")
def mywish(id):
    return render_template("my_wish.html", id=id)


@application.route("/my_info/<id>/")
def mypersonal(id):
    data = DB.get_user_info(id)
    return render_template("my_info.html", id=id, data=data)


# 그외
@application.route("/dynamicurl/<varible_name>/")
def DynamicUrl(variable_name):
    return str(variable_name)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
