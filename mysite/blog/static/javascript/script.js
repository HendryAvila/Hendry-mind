document.addEventListener("DOMContentLoaded", () => {
    // Selecciona TODOS los formularios con clase "form"
    const forms = document.querySelectorAll(".form");
    
    // Función genérica para validación de emails
    const validateEmailField = (emailInput) => {
        const container = emailInput.closest(".share-email__container-input-box, .comment-post__container-input-box");
        const errorSpan = container?.querySelector(".input__error-message");
        const isValid = isValidEmail(emailInput.value);

        if (!isValid) {
            errorSpan.textContent = "Please, add a correct email address. Example: yourEmail@example.com";
            emailInput.classList.add("invalid");
            emailInput.classList.remove("valid");
        } else {
            errorSpan.textContent = "";
            emailInput.classList.remove("invalid");
            emailInput.classList.add("valid");
        }
        return isValid;
    };

    // Función genérica para campos requeridos
    const validateRequiredField = (input) => {
        const container = input.closest(".share-email__container-input-box, .comment-post__container-input-box");
        const errorSpan = container?.querySelector(".input__error-message");
        const isValid = input.value.trim() !== "";

        if (!isValid) {
            errorSpan.textContent = "This field is required, please fill it.";
            input.classList.add("invalid");
            input.classList.remove("valid");
        } else {
            errorSpan.textContent = "";
            input.classList.remove("invalid");
            input.classList.add("valid");
        }
        return isValid;
    };

    // Aplica a todos los formularios
    forms.forEach(form => {
        const emailFields = form.querySelectorAll('input[type="email"]');
        const requiredFields = form.querySelectorAll("[required]");

        // Eventos para emails
        emailFields.forEach(email => {
            email.addEventListener("input", () => validateEmailField(email));
            email.addEventListener("blur", () => validateEmailField(email));
        });

        // Eventos para campos requeridos (excepto emails ya manejados)
        requiredFields.forEach(field => {
            if (field.type !== "email") {
                field.addEventListener("input", () => validateRequiredField(field));
                field.addEventListener("blur", () => validateRequiredField(field));
            }
        });

        // Validación al enviar
        form.addEventListener("submit", event => {
            event.preventDefault();
            let isFormValid = true;

            // Validar emails
            emailFields.forEach(email => {
                if (!validateEmailField(email)) isFormValid = false;
            });

            // Validar requeridos
            requiredFields.forEach(field => {
                if (field.type === "email") return;
                if (!validateRequiredField(field)) isFormValid = false;
            });

            if (isFormValid) form.submit();
        });
    });
});

function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}