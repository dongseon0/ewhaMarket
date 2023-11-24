from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()


@application.route("/")
def hello():
    # return render_template("index.html")
    return redirect(url_for('view_list'))


@application.route("/product_list")
def view_list():
    # html에 페이지 인덱스 클릭할 때마다 get으로 받아옴
    page = request.args.get("page", 0, type=int)
    per_page = 12  # item count to display per page
    per_row = 3  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)  # 페이지 인덱스로 start_idx, end_idx 생성
    data = DB.get_items()  # read the table
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


@application.route("/reg_item")
def reg_item():
    if session.get('id') is None:
        flash("로그인하쇼")
        return render_template("login.html")
    else:
        return render_template("reg_item.html")


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    data_key = DB.insert_item(data, image_file.filename, id=session.get('id'))
    return redirect(url_for('view_item_detail', key=data_key))


@application.route("/view_detail/<key>/")
def view_item_detail(key):
    # get_item_byname 상품 이름으로 데이터 가져오는 함수 생성
    data = DB.get_item_bykey(str(key))
    return render_template("details_of_item.html", key=key, data=data)


@application.route("/reg_review/<name>/")
def reg_review_init(name):
    if session.get('id') is None:
        flash("로그인하쇼")
        return render_template("login.html")
    else:
        return render_template("reg_review.html", id=session.get('id'), name=name)


@application.route("/reg_review", methods=['POST'])
def reg_review():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    name = data.get('productName')
    DB.reg_review(data, image_file.filename, id=session.get('id'))
    return redirect(url_for('view_review', name=name))


@application.route("/details_of_review/<name>/")
def view_review(name):
    data = DB.get_review(str(name))
    return render_template("details_of_review.html", id=session.get('id'), name=name, data=data)


@application.route("/user_reviews")
def view_reviews():
    page = request.args.get("page", 0, type=int)
    per_page = 5  # item count to display per page
    per_row = 1  # item count to display per row
    row_count = int(per_page/per_row)
    start_idx = per_page*page
    end_idx = per_page*(page+1)  # 페이지 인덱스로 start_idx, end_idx 생성
    data = DB.get_reviews()  # read the table
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
        total=item_counts
    )


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
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")


@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))


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


@application.route("/my_page")
def mypage():
    return render_template("my_page.html")


@application.route("/my_reviews")
def myreview():
    return render_template("my_reviews.html")


@application.route("/my_wish")
def wish():
    return render_template("my_wish.html")


@application.route("/my_info")
def personal():
    return render_template("my_info.html")


@application.route("/dynamicurl/<varible_name>/")
def DynamicUrl(variable_name):
    return str(variable_name)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
