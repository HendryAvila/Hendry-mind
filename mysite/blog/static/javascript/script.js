document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".form");

    if (!form) return;

    const nameInput = document.querySelector(".form input[name='name']");
    const emailElements = document.querySelectorAll(".share-email__email");

    // Función para validar el campo de Name
    function validateName() {
        const nameErrorSpan = nameInput.closest(".share-email__container-input-box")?.querySelector(".input__error-message");
        if (nameInput.validity.valueMissing) {
            nameErrorSpan.textContent = "This field is required, please fill it.";
            nameInput.classList.add("invalid");
            nameInput.classList.remove("valid");
        } else {
            nameErrorSpan.textContent = "";
            nameInput.classList.remove("invalid");
            nameInput.classList.add("valid");
        }
    }

    // Función para validar emails individualmente
    function validateEmail(email) {
        const errorSpan = email.closest(".share-email__container-input-box")?.querySelector(".input__error-message");
        if (!isValidEmail(email.value)) {
            errorSpan.textContent = "Please, add a correct email address. Example: yourEmail@example.com";
            email.classList.add("invalid");
            email.classList.remove("valid");
        } else {
            errorSpan.textContent = "";
            email.classList.remove("invalid");
            email.classList.add("valid");
        }
    }

    // Eventos para validación en tiempo real
    if (nameInput) {
        nameInput.addEventListener("input", validateName);
        nameInput.addEventListener("blur", validateName);
    }

    emailElements.forEach((email) => {
        email.addEventListener("input", () => validateEmail(email));
        email.addEventListener("blur", () => validateEmail(email));
    });

    // Validación en submit
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        let isValid = true;

        if (nameInput) {
            validateName();
            if (nameInput.classList.contains("invalid")) isValid = false;
        }

        emailElements.forEach((email) => {
            validateEmail(email);
            if (email.classList.contains("invalid")) isValid = false;
        });

        if (isValid) {
            form.submit();
        }
    });
});

// Función de validación de email
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}
