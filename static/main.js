// Select the menu button
const toggleButton = document.querySelector('.navbar__toogleBtn');
// Select the menu
const menu = document.querySelector('.navbar__menu');

// Add a click event listener to the menu button
toggleButton.addEventListener('click', () => {
    // Toggle the "active" class on the menu to show/hide it
    menu.classList.toggle('active');
});