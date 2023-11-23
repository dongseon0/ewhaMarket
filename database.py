import pyrebase
import json


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

#user db
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        if str(users.val()) == "None":  # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
        return True

    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value = []
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False

#상품db
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
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True

    def get_items(self):
        items = self.db.child("item").get().val()
        return items

    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value = ""
        print("###########", name)
        for res in items.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value


#리뷰db
    def insert_review(self, name, data, img_path):
        review_info = {
            "reviewTitle": data["reviewTitle"],
            "reviewContents": data["reviewContents"],
            "starsVariable": data["starsVariable"],
            "img_path": img_path
        }
        self.db.child("review").child(name).set(review_info)
        return True
        
    def get_reviews(self):
        reviews = self.db.child("review").get().val()
        return reviews

    def get_review_byname(self, name):
        reviews = self.db.child("review").get()
        target_value = ""
    
        for res in reviews.each():
            key_value = res.key()

            if key_value == name:
                target_value = res.val()
        return target_value