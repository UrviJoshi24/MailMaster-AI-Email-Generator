// Modal handling for Register
var registerModal = document.getElementById("registerModal");
var openRegisterBtn = document.getElementById("openRegisterModal");
var closeRegisterBtn = document.getElementById("closeRegisterModal");

openRegisterBtn.onclick = function() {
    registerModal.style.display = "block";
}

closeRegisterBtn.onclick = function() {
    registerModal.style.display = "none";
}

// Modal handling for Login
var loginModal = document.getElementById("loginModal");
var openLoginModalBtn = document.getElementById("openModalBtn");
var closeLoginModalBtn = document.getElementById("closeModalBtn");

openLoginModalBtn.onclick = function() {
    loginModal.style.display = "block";
}

closeLoginModalBtn.onclick = function() {
    loginModal.style.display = "none";
}

// Close modal if user clicks outside of it
window.onclick = function(event) {
    if (event.target == registerModal) {
        registerModal.style.display = "none";
    }
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
}

// Open login modal if redirected with ?login=true
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('login') === 'true') {
        loginModal.style.display = "block";
    }
}
