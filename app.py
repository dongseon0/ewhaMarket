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
    # 페이지 및 페이징 관련 변수들 설정
    page = request.args.get("page", 0, type=int)
    per_page = 6  # 페이지당 아이템 수
    per_row = 3  # 한 줄에 표시할 아이템 수
    start_idx = per_page * page
    end_idx = per_page * (page + 1)

    # 데이터 로드 및 페이지에 따른 필요한 데이터 가져오기
    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    # 데이터를 행 단위로 나누어 저장할 리스트 생성
    data_rows = []

    for i in range(per_row):
        if (i == per_row-1) and (tot_count % per_row != 0):
            # 남은 데이터가 행에 모두 들어가지 않을 경우의 처리
            data_rows.append(dict(list(data.items())[i*per_row:]))
        else:
            data_rows.append(dict(list(data.items())[i*per_row:(i+1)*per_row]))

    # render_template에 전달할 데이터 생성
    template_data = {
        "datas": data.items(),
        "limit": per_page,
        "page": page,
        "page_count": int((item_counts / per_page) + 1),
        "total": item_counts
    }

    # data_rows에 저장된 데이터를 'row1', 'row2' 등으로 전달
    for i, row_data in enumerate(data_rows):
        template_data[f"row{i+1}"] = row_data.items()

    return render_template("product_list.html", **template_data)


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


@application.route("/signup")
def signup():
    return render_template("signup.html")


@application.route("/my_page")
def mypage():
    return render_template("my_page.html")


@application.route("/my_reviews")
def myreview():
    return render_template("myreviews.html")


@application.route("/my_wish")
def wish():
    return render_template("my_wish.html")


@application.route("/my_info")
def personal():
    return render_template("my_info.html")


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


@application.route("/dynamicurl/<varible_name>/")
def DynamicUrl(variable_name):
    return str(variable_name)


@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:", name)
    # get_item_byname 상품 이름으로 데이터 가져오는 함수 생성
    data = DB.get_item_byname(str(name))
    print("####data:", data)
    return render_template("submit_item_result.html", name=name, data=data)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
