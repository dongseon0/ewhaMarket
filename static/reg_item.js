function div_OnOff(myId, yourId) {
    document.getElementById(myId).style.display = "";
    document.getElementById(yourId).style.display = "none";
}

function checkInput(){
    var name = document.getElementById("name");
    var namevalue = name.value;
    
    if(!namevalue){
        alert("상품명을 입력하세요.");
        return false;
    }
}