// Select the menu button
const toggleButton = document.querySelector('.navbar__toogleBtn');
// Select the menu
const menu = document.querySelector('.navbar__menu');

// Add a click event listener to the menu button
toggleButton.addEventListener('click', () => {
    // Toggle the "active" class on the menu to show/hide it
    menu.classList.toggle('active');
});

// 로그인 여부에 따라 네비바 버튼 바꾸기
// var isLogin = true;
// var loginBtn = document.getElementById("nav-login");
// var signupBtn = document.getElementById("nav-signup");
// loginBtn.addEventListener("click", login);
// signupBtn.addEventListener("click", login);

// function login() {
//     document.getElementById("nav-login").innerHTML="마이 페이지";
//     document.getElementById("nav-signup").innerHTML="로그아웃";
// }
// function logout() {
//     document.getElementById("nav-login").innerHTML="로그인";
//     document.getElementById("nav-signup").innerHTML="회원가입";
// }