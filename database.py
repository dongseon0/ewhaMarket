import pyrebase
import json
from datetime import datetime

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

    # 프로필 사진 변경하기
    def set_profile_image(self, id, img_path):
        self.db.child("users").child(id).child(
            "user_info").child("profile").set(img_path)
        return True

    # 특정 아이디의 프로필 사진 불러오기
    def get_profile_image_path_byid(self, id):
        profile = self.db.child("users").child(id).child(
            "user_info").get().val().get('profile')
        if profile == None or profile == "":
            return "default.png"
        else:
            return profile

    # 상품
    # 상품 추가
    def insert_item(self, data, img_path, id):
        item_info = { # item_info 딕셔너리에 id값과 상품 등록 시 입력되었던 input값들 추가
            "sellerId": id,
            "name": data["name"],
            "description": data["description"],
            "location": data["location"],
            "quantity": data["quantity"],
            "category": data["category"],
            "phone": data["phone"],
            "img_path": img_path,
        }
        # select-status-button라는 name을 가진 radio버튼의 value값을 검사
        # status키값에 적절한 value값 저장
        if data["select-status-button"] == "new":
            item_info["status"] = "새 상품"
        elif data["select-status-button"] == "lnew":
            item_info["status"] = "거의 새 상품"
        else:
            item_info["status"] = "중고 상품"

        # select-transaction-method-button라는 name을 가진 radio버튼의 value값을 검사
        # method키값에 적절한 value값 저장
        if data["select-transaction-method-button"] == "delivery":
            item_info["method"] = "택배 거래"
        else:
            item_info["method"] = "직거래"

        item_data = self.db.child("users").child(
            id).child("user_list").push(str(data["name"]))
        item_key = item_data['name']
        self.db.child("items").child(item_key).set(item_info)
        # select-pricing-button라는 name을 가진 radio버튼의 value값을 검사
        # 경매면 auction_info 딕셔너리 생성 후 입력값 저장
        # 고정가격이면 fixed_info 딕셔너리 생성 후 입력값 저장
        if data["select-pricing-button"] == "경매":
            auction_info = {
                "winner": "",
                "currentPrice": int(data["start-price"]),
                "startDate": data["start-date"],
                "startTime": data["start-time"],
                "endDate": data["end-date"],
                "endTime": data["end-time"],
                "selectRisingPrice": int(data["select-rising-price"]),
                "isAuction": True
            }
            self.db.child("items").child(item_key).update(auction_info)
        elif data["select-pricing-button"] == "고정가격":
            fixed_info = {
                "fixedPrice": data["fixed-price"],
                "isAuction": False
            }
            self.db.child("items").child(item_key).update(fixed_info)
        return item_key

    # 상품 가져오기
    def get_items(self):
        items = self.db.child("items").get().val()
        return items

    # 키값으로 상품 가져오기
    def get_item_bykey(self, key):
        items = self.db.child("items").get()
        target_value = ""
        for res in items.each():
            key_value = res.key()

            if key_value == key:
                target_value = res.val()
        return target_value

    # 경매 상품 가져오기
    def get_is_auction_status(self, key):
        item_data = self.db.child("items").child(key).get().val()
        if item_data:
            is_auction = item_data.get("isAuction")
            if is_auction is not None:
                return is_auction
        return None  # Or handle the case where isAuction is not found

    # 경매 가격, 입찰자 데베에 적용하기
    def set_auction(self, key, selectRisingPrice, id):
        self.db.child("items").child(key).update({"winner": id})
        currentPrice = self.db.child("items").child(
            key).get().val().get("currentPrice")
        self.db.child("items").child(key).update(
            {"currentPrice": (int(currentPrice) + int(selectRisingPrice))})
        return True

    # 찜한 상품 가져오기
    def get_items_byheart(self, id):
        items = self.db.child("users").child(id).child("user_wish").get()
        target_value = []
        target_key = []
        if items.each():
            for res in items.each():
                value = res.val()
                key_value = res.key()
                if value['interested'] == "Y":
                    target_key.append(key_value)
                    target_value.append(self.db.child(
                        "items").child(key_value).get().val())
        new_dict = {}
        for k, v in zip(target_key, target_value):
            new_dict[k] = v
        return new_dict

    # 카테고리 별로 상품 가져오기
    def get_items_bycategory(self, cate):
        items = self.db.child("items").get()
        target_value = []
        target_key = []
        for res in items.each():
            value = res.val()
            key_value = res.key()

            if value['category'] == cate:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value", target_value)
        new_dict = {}

        for k, v in zip(target_key, target_value):
            new_dict[k] = v

        return new_dict

    # 찜하기 기능
    def get_heart_bykey(self, uid, key):
        hearts = self.db.child("users").child(uid).child("user_wish").get()

        target_value = ""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

            if key_value == key:
                target_value = res.val()
        return target_value

    def update_heart(self, uid, isHeart, key):
        heart_info = {
            "interested": isHeart
        }
        if isHeart == "Y":
            self.db.child("items").child(key).child(
                "hearts").child(uid).set(heart_info)
        else:
            self.db.child("items").child(key).child(
                "hearts").child(uid).remove()

        self.db.child("users").child(uid).child(
            "user_wish").child(key).set(heart_info)
        return True

    # 상품 삭제
    def delete_item_bykey(self, key, sellerId):
        self.db.child("users").child(sellerId).child(
            "user_list").child(key).remove()
        hearts = self.db.child("items").child(key).child("hearts").get()
        if hearts.each():
            for heart in hearts.each():
                heartId = heart.key()
                self.db.child("users").child(heartId).child(
                    "user_wish").child(key).remove()
        self.db.child("items").child(key).remove()
        return True

    # 유저 판매내역 가져오기
    def get_lists(self, id):
        user_list = self.db.child("users").child(id).child("user_list").get()
        matched_items = {}
        if not user_list.each():
            return matched_items
        else:
            user_list_keys = [item.key() for item in user_list.each()]

        items = self.db.child("items").get()
        for item in items.each():
            if item.key() in user_list_keys:
                matched_items[item.key()] = item.val()

        return matched_items

    def get_lists_bykey(self, key):
        items = self.db.child("users").child(id).child("user_lists").get()
        target_value = ""
        for res in items.each():
            key_value = res.key()

            if key_value == key:
                target_value = res.val()
        return target_value

    # 리뷰
    # 리뷰 데이터베이스에 등록하기
    def reg_review(self, data, img_path, buyerId, sellerId):
        if img_path == "": # 이미지 없으면 빈 이미지 등록
            img_path = "empty.jpeg"
        
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

    # 키값으로 데이터베이스에서 특정 리뷰 불러오기
    def get_review_bykey(self, key, sellerId):
        reviews = self.db.child("users").child(
            sellerId).child("user_reviews").get()
        target_value = ""
        for res in reviews.each():
            key_value = res.key()

            if key_value == key:
                target_value = res.val()
        return target_value
    
    # 특정 리뷰 삭제하기
    def delete_review_bykey(self, key, sellerId):
        self.db.child("users").child(sellerId).child("user_reviews").child(key).remove()
        return True

    # 특정 아이디의 리뷰들을 데이터베이스에서 불러오기
    def get_reviews(self, sellerId):
        items = self.db.child("users").child(sellerId).child("user_reviews").get().val()
        return items

    # 특정 아이디의 리뷰 평점 평균 계산하기
    def get_reviews_star_avg(self, sellerId):
        reviews = self.db.child("users").child(sellerId).child("user_reviews").get()

        if not reviews.each():
            return 0      
        
        stars = 0
        starCount = 0
        for review in reviews.each():
            stars += int(review.val().get("starsVariable")) + 1
            starCount += 1
        return round(float(stars) / starCount, 1)

    # 데이터베이스에서 특정 리뷰 하트 정보 불러오기
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

    # 데이터베이스에서 특정 리뷰 하트 정보 불러오기
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

    # 데이터베이스에서 특정 아이디의 리뷰 하트 정보 불러오기
    def get_review_heart_bykey(self, id, key, sellerId):
        heart = self.db.child("users").child(
            sellerId).child("user_reviews").child(key).child("hearts").child(id).get()

        if heart.val() == None:
            return ""
        else:
            return heart.val()

    # 데이터베이스에서 특정 아이디의 리뷰 하트 정보 업데이트하기
    def update_review_heart(self, id, key, sellerId, heart):
        if int(heart) == 0:
            self.db.child("users").child(sellerId).child("user_reviews").child(
                key).child("hearts").child(id).remove()
            return True

        heart_info = {
            "heart": int(heart)
        }
        self.db.child("users").child(sellerId).child("user_reviews").child(
            key).child("hearts").child(id).set(heart_info)

        if int(heart) == 1:
            return True
        elif int(heart) == -1:
            return True

    # 마이페이지_개인정보
    def get_user_info(self, id):
        items = self.db.child("users").child(id).child("user_info").get().val()
        return items
