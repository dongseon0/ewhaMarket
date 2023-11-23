import pyrebase
import json


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def reg_review(self, data, img_path):
        review_info = {
            "reviewTitle": data["reviewTitle"],
            "reviewContents": data["reviewContents"],
            "starsVariable": data["starsVariable"],
            "img_path": img_path
        }
        self.db.child("review").child(data["productName"]).set(review_info)
        return True

    def get_review(self, name):
        items = self.db.child("review").child(name).get().val()
        return items

    def insert_item(self, name, data, img_path):
        item_info = {
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
        self.db.child("item").push(item_info)
        return True

    def insert_user(self, data, pw):
        user_info = {
            "pw": pw,
            "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("users").child(data['id']).child("user_info").set(user_info)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("users").get()
        if str(users.val()) == "None":  # 첫 회원가입
            return True
        else:
            if id_string in users.val():
                return False
        return True

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

    def get_items(self):
        items = self.db.child("item").get().val()
        return items

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value = ""
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value
