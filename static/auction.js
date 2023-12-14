// 경매 오픈했는지, 종료했는지, 진행 중이라면 얼마나 남았는지 체크하는 함수
function remainingTime(element) {
    // 데이터베이스 정보 불러와서 시작시간, 종료시간 변수로 설정하기
    var startDate = element.getAttribute('data-start-date').split("-");
    var startTime = element.getAttribute('data-start-time').split(":");
    var endDate = element.getAttribute('data-end-date').split("-");
    var endTime = element.getAttribute('data-end-time').split(":");

    var open = new Date(Number(startDate[0]), Number(startDate[1]) - 1, Number(startDate[2]), Number(startTime[0]), Number(startTime[1]));
    var end = new Date(Number(endDate[0]), Number(endDate[1]) - 1, Number(endDate[2]), Number(endTime[0]), Number(endTime[1]));

    var ot = open.getTime();
    var et = end.getTime();

    // 현재 시간 체크
    var now = new Date();
    var nt = now.getTime();

    if (parseInt(nt) < parseInt(ot)) // 오픈 전
    {
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

        if (day > 0)
            element.innerHTML = "오픈까지 " + day + "일 " + hour + "시간 " + min + "분 ";
        else
            element.innerHTML = "오픈까지 " + hour + "시간 " + min + "분 ";
    }
    else if (parseInt(nt) > parseInt(et)) // 종료
    {
        auctionState = false;
        element.innerHTML = "종료되었습니다."
    }
    else // 진행 중
    {
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

        if (day > 0)
            element.innerHTML = "종료까지 " + day + "일 " + hour + "시간 " + min + "분 ";
        else
            element.innerHTML = "종료까지 " + hour + "시간 " + min + "분 ";
    }
}

// 경매 상품이라면 매 초마다 함수 실행하게끔 설정하기
document.addEventListener("DOMContentLoaded", function () {
    var auctionStates = document.querySelectorAll('.auction-state');
    auctionStates.forEach(function (element) {
        remainingTime(element);
        setInterval(function () {
            remainingTime(element);
        }, 1000);
    });
});