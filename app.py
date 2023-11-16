from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()


@application.route("/")
def hello():
    return render_template("index.html")


@application.route("/list")
def view_list():
    return render_template("list.html")


@application.route("/review")
def view_review():
    return render_template("review.html")


@application.route("/reg_items")
def reg_item():
    return render_template("reg_item.html")


@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")


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


@application.route("/mypage")
def mypage():
    return render_template("mypage.html")


@application.route("/myreview")
def myreview():
    return render_template("myreview.html")


@application.route("/wish")
def wish():
    return render_template("wish.html")


@application.route("/personal")
def personal():
    return render_template("personal.html")


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


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
