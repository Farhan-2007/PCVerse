// ================= Login Password =================

const loginToggle = document.getElementById("togglePassword");
const loginPassword = document.getElementById("password");

if (loginToggle && loginPassword) {

    loginToggle.addEventListener("click", function () {

        if (loginPassword.type === "password") {

            loginPassword.type = "text";
            this.textContent = "🙈";

        } else {

            loginPassword.type = "password";
            this.textContent = "👁";

        }
    });
}

// ================= Signup Password =================

const signupToggle = document.getElementById("toggleSignupPassword");
const signupPassword = document.getElementById("signupPassword");

if (signupToggle && signupPassword) {

    signupToggle.addEventListener("click", function () {

        if (signupPassword.type === "password") {

            signupPassword.type = "text";
            this.textContent = "🙈";

        } else {

            signupPassword.type = "password";
            this.textContent = "👁";

        }
    });
}