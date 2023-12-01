if (document.getElementById("currentPrice") == "") {
    var get_current_price = document.getElementById("startPrice");
} else {
    var get_current_price = document.getElementById("currentPrice");
}
var get_risingPrice = document.getElementById("selectRisingPrice");
var current_price = parseInt(get_current_price.innerHTML, 10);
var risingPrice = parseInt(get_risingPrice.innerHTML, 10);

document.getElementById("current").innerHTML = current_price + "원";

function click_btn_money() {
    current_price = current_price + risingPrice;
    document.getElementById("current").innerHTML = current_price + "원";
}

function auction() {
    // url = '/auction/{{key}}/' + current_price;
    $.ajax({
        type: 'POST',
        url: '/auction/{{key}}/' + current_price,
        data: {},
        success: function (response) {
            alert(response['msg']);
        }
    });
}

const btnMoney = document.getElementById("btnMoney");
btnMoney.addEventListener("click", click_btn_money);
btnMoney.addEventListener("click", auction);

// 버튼 이름 바꾸기
if (risingPrice == 1000) {
    btnMoney.value = "▲천원"
} else if (risingPrice == 5000) {
    btnMoney.value = "▲5천원"
} else if (risingPrice == 10000) {
    btnMoney.value = "▲만원"
} else if (risingPrice == 50000) {
    btnMoney.value = "▲5만원"
}

// 기존 코드
function showHeart() {
    $.ajax({
        type: 'GET',
        url: '/show_heart/{{key}}/',
        data: {},
        success: function (response) {
            updateHeartButton(response['my_heart']);
        }
    });
}

function updateHeartButton(myHeart) {
    if (myHeart['interested'] === 'Y') {
        $(".btn-love").css("background-color", "#c1e6ff");
        $(".btn-love").css("color", "#003742");
        $(".btn-love").css("border", "3px solid #c1e6ff");
        $(".btn-love").val("♥ 찜하기");
        $(".btn-love").attr("onclick", "unlike()");
    } else {
        $(".btn-love").attr("onclick", "like()");
    }
}

function like() {
    $.ajax({
        type: 'POST',
        url: '/like/{{key}}/',
        data: {
            interested: "Y"
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload();
        },
        error: function (xhr, status, error) {
            handleRequestError(xhr);
        }
    });
}

function unlike() {
    $.ajax({
        type: 'POST',
        url: '/unlike/{{key}}/',
        data: {
            interested: "N"
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload();
        },
        error: function (xhr, status, error) {
            handleRequestError(xhr);
        }
    });
}

function handleRequestError(xhr) {
    var response = xhr.responseJSON;
    if (response && response.error) {
        alert(response.error);
        if (response.redirect_url) {
            window.location.href = response.redirect_url;
        }
    } else {
        alert('알 수 없는 오류가 발생했습니다.');
    }
}

$(document).ready(function () {
    showHeart();
});