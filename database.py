import pyrebase
import json


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    # 회원가입
    def insert_user(self, data, pw):
        user_info = {
            "pw": pw,
            "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("users").child(data['id']).child(
                "user_info").set(user_info)
            return True
        else:
            return False

    # 회원가입 시 중복 체크
    def user_duplicate_check(self, id_string):
        users = self.db.child("users").get()
        if str(users.val()) == "None":  # 첫 회원가입
            return True
        else:
            if id_string in users.val():
                return False
        return True

    # 로그인
    def find_user(self, id, pw):
        users = self.db.child("users").get()
        for user in users.each():
            user_id = user.key()
            if user_id == id:
                user_data = user.val()
                user_info = user_data.get("user_info")
                if user_info.get("pw") == pw:
                    return True
                else:
                    return False
        return False

    # 상품
    def insert_item(self, data, img_path, id):
        item_info = {
            "sellerId": id,
            "name": data["name"],
            "status": data["status"],
            "description": data["description"],
            "method": data["method"],
            "location": data["location"],
            "quantity": data["quantity"],
            "category": data["category"],
            "tag": data["tag"],
            "phone": data["phone"],
            "img_path": img_path
        }
        item_data = self.db.child("users").child(
            id).child("user_list").push(str(data["name"]))
        item_key = item_data['name']
        self.db.child("items").child(item_key).set(item_info)
        return item_key

    def get_items(self):
        items = self.db.child("items").get().val()
        return items

    def get_item_bykey(self, key):
        items = self.db.child("items").get()
        target_value = ""
        for res in items.each():
            key_value = res.key()

            if key_value == key:
                target_value = res.val()
        return target_value

    # 리뷰
    def reg_review(self, data, img_path, buyerId, sellerId):
        review_info = {
            "sellerId": sellerId,
            "buyerId": buyerId,
            "reviewTitle": data["reviewTitle"],
            "reviewContents": data["reviewContents"],
            "starsVariable": data["starsVariable"],
            "img_path": img_path
        }
        review_data = self.db.child("users").child(
            sellerId).child("user_reviews").push(review_info)
        review_key = review_data['name']
        return review_key

    def get_review_bykey(self, key, sellerId):
        reviews = self.db.child("users").child(
            sellerId).child("user_reviews").get()
        target_value = ""
        for res in reviews.each():
            key_value = res.key()

            if key_value == key:
                target_value = res.val()
        return target_value

    def get_reviews(self, sellerId):
        items = self.db.child("users").child(
            sellerId).child("user_reviews").get().val()
        return items

    def get_review_good_bykey(self, key, sellerId):
        hearts = self.db.child("users").child(
            sellerId).child("user_reviews").child(key).child("hearts").get()

        good = 0
        if not hearts.each():
            return good

        for heart in hearts.each():
            heart1 = heart.val().get("heart")

            if heart1 == 1:
                good += 1
        return good

    def get_review_bad_bykey(self, key, sellerId):
        hearts = self.db.child("users").child(
            sellerId).child("user_reviews").child(key).child("hearts").get()

        bad = 0
        if not hearts.each():
            return bad

        for heart in hearts.each():
            heart1 = heart.val().get("heart")

            if heart1 == -1:
                bad += 1
        return bad

    def get_review_heart_bykey(self, id, key, sellerId):
        heart = self.db.child("users").child(
            sellerId).child("user_reviews").child(key).child("hearts").child(id).get()

        if heart.val() == None:
            return ""
        else:
            return heart.val()

    def update_review_heart(self, id, key, sellerId, heart):
        heart_info = {
            "heart": int(heart)
        }
        self.db.child("users").child(sellerId).child("user_reviews").child(
            key).child("hearts").child(id).set(heart_info)
        return True

    # 마이페이지
    def get_user_info(self, id):
        items = self.db.child("users").child(id).child("user_info").get().val()
        return items
