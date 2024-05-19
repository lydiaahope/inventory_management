document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('#login-form');
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        // Here you will handle the login logic
        alert('Login Attempted!');
    });
});
