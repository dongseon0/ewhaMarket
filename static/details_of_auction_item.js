var get_current_price = document.getElementById("currentPrice");
var get_risingPrice = document.getElementById("selectRisingPrice");
var current_price = parseInt(get_current_price.innerHTML, 10);
var risingPrice = parseInt(get_risingPrice.innerHTML, 10);
document.getElementById("current").innerHTML = current_price + "원";

var auctionState = false;
function auction() {
    if (auctionState == true) {
        $.ajax({
            type: 'POST',
            url: '/auction/' + document.getElementById("key").innerHTML + '/' + document.getElementById("seller-id").innerHTML + '/' + risingPrice,
            data: {},
            success: function (response) {
                alert(response['msg']);
                window.location.reload();
            }
        });
    } else {
        alert("입찰할 수 없습니다.");
    }
}

const btnMoney = document.getElementById("btnMoney");
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

var startDate = document.getElementById("start-date").innerHTML.split("-");
var startTime = document.getElementById("start-time").innerHTML.split(":");
var endDate = document.getElementById("end-date").innerHTML.split("-");
var endTime = document.getElementById("end-time").innerHTML.split(":");

function remaingTime() {
    var now = new Date();
    var open = new Date(parseInt(startDate[0]), parseInt(startDate[1]) - 1, parseInt(startDate[2]), parseInt(startTime[0]), parseInt(startTime[1]));
    var end = new Date(parseInt(endDate[0]), parseInt(endDate[1]) - 1, parseInt(endDate[2]), parseInt(endTime[0]), parseInt(endTime[1]));

    var nt = now.getTime();
    var ot = open.getTime();
    var et = end.getTime();

    if (parseInt(nt) < parseInt(ot)) { // 오픈 전
        auctionState = false;
        sec = parseInt(ot - nt) / 1000;
        day = parseInt(sec / 60 / 60 / 24);
        sec = (sec - (day * 60 * 60 * 24));
        hour = parseInt(sec / 60 / 60);
        sec = (sec - (hour * 60 * 60));
        min = parseInt(sec / 60);
        sec = parseInt(sec - (min * 60));
        if (hour < 10) { hour = "0" + hour; }
        if (min < 10) { min = "0" + min; }
        if (sec < 10) { sec = "0" + sec; }

        document.getElementById("auction-state").innerHTML = "오픈까지 "
        document.getElementById("remaining-hour").innerHTML = hour + "시간 ";
        document.getElementById("remaining-minute").innerHTML = min + "분 ";
        document.getElementById("remaining-second").innerHTML = sec + "초";
    } else if (parseInt(nt) > parseInt(et)) { // 마감
        auctionState = false;
        document.getElementById("auction-state").innerHTML = "종료되었습니다."
        document.getElementById("remaining-hour").innerHTML = "";
        document.getElementById("remaining-minute").innerHTML = "";
        document.getElementById("remaining-second").innerHTML = "";
    } else { // 진행
        auctionState = true;
        sec = parseInt(et - nt) / 1000;
        day = parseInt(sec / 60 / 60 / 24);
        sec = (sec - (day * 60 * 60 * 24));
        hour = parseInt(sec / 60 / 60);
        sec = (sec - (hour * 60 * 60));
        min = parseInt(sec / 60);
        sec = parseInt(sec - (min * 60));
        if (hour < 10) { hour = "0" + hour; }
        if (min < 10) { min = "0" + min; }
        if (sec < 10) { sec = "0" + sec; }

        document.getElementById("auction-state").innerHTML = "남은 시간: "
        document.getElementById("remaining-hour").innerHTML = hour + "시간 ";
        document.getElementById("remaining-minute").innerHTML = min + "분 ";
        document.getElementById("remaining-second").innerHTML = sec + "초";
    }
}
remaingTime();
setInterval(remaingTime, 1000);
