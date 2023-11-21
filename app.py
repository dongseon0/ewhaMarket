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


@application.route("/user_review")
def view_review():
    return render_template("user_review.html")


@application.route("/reg_item")
def reg_item():
    return render_template("reg_item.html")


@application.route("/reg_review")
def reg_review():
    return render_template("reg_review.html")


@application.route("/submit_item")
def reg_item_submit():
    name = request.args.get("name")
    status = request.args.get("status")
    description = request.args.get("description")
    method = request.args.get("method")
    location = request.args.get("location")
    quantity = request.args.get("quantity")
    category = request.args.get("category")
    tag = request.args.get("tag")
    phone = request.args.get("phone")

    # print(name,addr,tel,category,park,time,site)
    # return render_template("reg_item.html")


@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)
    return render_template("submit_item_result.html", data=data, img_path="static/images/{}".format(image_file.filename))


@application.route("/login")
def login():
    return render_template("login.html")


@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
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
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
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


@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:", name)
    # get_item_byname 상품 이름으로 데이터 가져오는 함수 생성
    data = DB.get_item_byname(str(name))
    print("####data:", data)
    return render_template("details_of_item.html", name=name, data=data)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
