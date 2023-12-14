// 가격 책정 방식 radio버튼 클릭 시 해당하는 div가 나타나고 그 반대의 div는 사라짐
function div_OnOff(myId, yourId) {
    document.getElementById(myId).style.display = "";
    document.getElementById(yourId).style.display = "none";
}

// onclick 이벤트 함수
// file 버튼을 클릭 시 img 요소를 삭제함
function clickFile() {
    var image = document.getElementById("img");
    image.parentNode.removeChild(image);
}

// onchange 이벤트 함수
// img라는 새로운 요소를 만들고 거기에 입력 받은 이미지를 추가함
function loadFile(input) {
    var file = input.files[0];

    var image = document.createElement("img");
    image.setAttribute("class", 'img');
    image.setAttribute("id", 'img');

    image.src = URL.createObjectURL(file);

    image.style.width = "100%";
    image.style.height = "100%";
    image.style.objectFit = "cover";

    var container = document.getElementById('image-show');
    container.appendChild(image);
    $('#image-show').attr('value', 1);
}

// input값을 검사하는 함수
// submit 버튼을 눌렀을 때 실행
// input값이 없거나 시각을 잘못 설정하면 alert를 띄움
function checkInput(){
    // 요소들로부터 value값을 가져옴
    // input이 없을 시 value가 null임
    var image = document.getElementById("file").value;
    var description = document.getElementById("description").value;
    var quantity = document.getElementById("quantity").value;
    var selectPricingValue = $('input[name=select-pricing-button]:checked').val();
    var name = document.getElementById("name").value;
    var location = document.getElementById("location").value;
    var phone = document.getElementById("phone").value;
    var fixedPrice = document.getElementById("fixedPrice").value;
    var startPrice = document.getElementById("startPrice").value;
    var checkStartDate = document.getElementById("startDate").value;
    var checkStartTime = document.getElementById("startTime").value;
    var checkEndDate = document.getElementById("endDate").value;
    var checkEndTime = document.getElementById("endTime").value;

    // 시간을 비교하기 위해 입력 받은 시간을 밀리세컨드로 변환함
    var startDate = checkStartDate.split("-");
    var startTime = checkStartTime.split(":");
    var endDate = checkEndDate.split("-");
    var endTime = checkEndTime.split(":");
    var now = new Date();
    var start = new Date(parseInt(startDate[0]), parseInt(startDate[1]) - 1, parseInt(startDate[2]), parseInt(startTime[0]), parseInt(startTime[1]));
    var end = new Date(parseInt(endDate[0]), parseInt(endDate[1]) - 1, parseInt(endDate[2]), parseInt(endTime[0]), parseInt(endTime[1]));
    var nt = now.getTime();
    var st = start.getTime();
    var et = end.getTime();

    // radio 버튼이 체크되었는지 검사하는 변수
    // boolean type
    var risingPrice = $('input:radio[name=select-rising-price]').is(':checked');
    var status = $('input:radio[name=select-status-button]').is(':checked');
    var method = $('input:radio[name=select-transaction-method-button]').is(':checked');
    var selectPricing = $('input:radio[name=select-pricing-button]').is(':checked');

    // 입력값이 없을 시 alert를 띄움
    if(!image) {
        alert("상품 이미지를 등록해주세요.");
        return false;
    }

    if(!name) {
        alert("상품명을 입력해주세요.");
        return false;
    }

    if(!status) {
        alert("상품 상태를 선택해주세요.");
        return false;
    }

    if(!description) {
        alert("상품 설명을 입력해주세요.");
        return false;
    }

    if(!method) {
        alert("거래 방식을 선택해주세요.");
        return false;
    }

    if(!location) {
        alert("선호 거래 지역을 입력해주세요.");
        return false;
    }

    if(!quantity) {
        alert("수량을 입력해주세요.");
        return false;
    }

    if(!selectPricing) {
        alert("가격 책정 방식을 선택해주세요");
        return false;
    }

    if(selectPricingValue == "고정가격") {
        if(!fixedPrice) {
            alert("가격을 입력해주세요.");
            return false;
        }
    }

    else {
        if(!startPrice) {
            alert("경매 시작가를 입력해주세요.");
            return false;
        }

        if(!risingPrice) {
            alert("경매 상승가를 선택해주세요.");
            return false;
        }

        if(!checkStartDate) {
            alert("경매 시작 날짜를 설정해주세요.");
            return false;
        }

        if(!checkStartTime) {
            alert("경매 시작 시간을 설정해주세요.");
            return false;
        }

        if(!checkEndDate) {
            alert("경매 종료 날짜를 설정해주세요.");
            return false;
        }

        if(!checkEndTime) {
            alert("경매 종료 시간을 설정해주세요.");
            return false;
        }
        
        // 시각이 잘못 입력 되었을 시 alert를 띄움
        if(parseInt(st) < parseInt(nt)) {
            alert("시작 시각을 현재 시각 후로 설정해주세요.");
            return false;
        }

        if(parseInt(et) < parseInt(st)) {
            alert("종료 시각을 시작 시각 후로 설정해주세요.");
            return false;
        }

    }

    if(!phone) {
        alert("연락처를 입력해주세요.");
        return false;
    }

}
