function div_OnOff(myId, yourId) {
    document.getElementById(myId).style.display = "";
    document.getElementById(yourId).style.display = "none";
}

function checkInput(){
    var description = document.getElementById("description").value;
    var quantity = document.getElementById("quantity").value;
    var selectPricingValue = $('input[name=select-pricing-button]:checked').val();
    var name = document.getElementById("name");
    var nameValue = name.value;
    var location = document.getElementById("location");
    var locationValue = location.value;
    var phone = document.getElementById("phone");
    var phoneValue = phone.value;
    var status = $('input:radio[name=select-status-button]').is(':checked');
    var method = $('input:radio[name=select-transaction-method-button]').is(':checked');
    var selectPricing = $('input:radio[name=select-pricing-button]').is(':checked');

    if(!nameValue) {
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

    if(!locationValue) {
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

    if(!phoneValue) {
        alert("연락처를 입력해주세요.");
        return false;
    }

}