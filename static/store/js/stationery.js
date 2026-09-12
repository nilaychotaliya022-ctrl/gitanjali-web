/* =========================================================
   STATIONERY PAGE ENHANCEMENTS
========================================================= */

document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".brand-card");

    cards.forEach(function (card, index) {
        card.style.setProperty("--stagger", index * 45 + "ms");
        card.classList.add("stationery-card-ready");
    });

    const heroCard = document.querySelector(".hero-product-card");

    if (heroCard) {
        heroCard.addEventListener("mousemove", function (event) {
            if (window.innerWidth <= 700) {
                return;
            }

            const rect = heroCard.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;

            heroCard.style.transform =
                "rotate(0deg) perspective(800px) rotateY(" +
                (x * 4) +
                "deg) rotateX(" +
                (y * -4) +
                "deg) translateY(-5px)";
        });

        heroCard.addEventListener("mouseleave", function () {
            heroCard.style.transform = "";
        });
    }
});
