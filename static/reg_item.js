function div_OnOff(v, id) {
    if(v == "고정가격") {
        document.getElementById(id).style.display = "";
    }
    else {
        document.getElementById(id).style.display = "none";
    }
}