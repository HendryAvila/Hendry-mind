"stric mode";

document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for "Back to top" link
    const backToTopLinks = document.querySelectorAll('a[href="#"]');
    backToTopLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    });

    // You can add more interactive features here in the future.
    // For example, a responsive navbar toggle or a theme switcher.
});

function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}