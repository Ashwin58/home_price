document.addEventListener("DOMContentLoaded", function () {
    // Form submission handling
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function () {
            const button = form.querySelector("button");
            button.innerHTML = "Processing...";
            button.disabled = true;
        });
    }

    // Smooth scrolling effect for internal navigation links
    document.querySelectorAll("nav ul li a").forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const href = this.getAttribute("href");

            // Check if the link is an internal section link (starts with #)
            if (href.startsWith("#")) {
                e.preventDefault(); // Prevent default behavior only for internal links
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop,
                        behavior: "smooth"
                    });
                }
            }
            // Allow default behavior for external links (e.g., /about, /logout, /home)
        });
    });

    // Fade-in effect for content
    const container = document.querySelector(".container");
    if (container) {
        container.style.opacity = 0;
        setTimeout(() => {
            container.style.transition = "opacity 1.5s ease-in-out";
            container.style.opacity = 1;
        }, 500);
    }

    // Background image slideshow
    const images = [
        "/static/images/image1.jpg",
        "/static/images/image2.webp",
        "/static/images/image3.jpg",
        "/static/images/image4.jpg"
    ];

    let index = 0;
    function changeBackground() {
        document.body.style.backgroundImage = `url(${images[index]})`;
        index = (index + 1) % images.length;
    }

    if (images.length > 0) {
        changeBackground();
        setInterval(changeBackground, 5000); // Change every 5 seconds
    }
});