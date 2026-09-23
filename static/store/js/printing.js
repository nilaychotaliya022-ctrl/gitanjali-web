/* =========================================================
   GITANJALI PRINTING PAGE — JAVASCRIPT
   Scroll reveal · image fallback · feature stagger
========================================================= */

(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {

        /* -------------------------------------------------
           MACHINE CARD SCROLL REVEAL
        ------------------------------------------------- */

        const machineCards = document.querySelectorAll(".machine-card");

        if (machineCards.length && "IntersectionObserver" in window) {

            const observer = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add("is-visible");
                            observer.unobserve(entry.target);
                        }
                    });
                },
                {
                    threshold: 0.12,
                    rootMargin: "0px 0px -60px 0px",
                }
            );

            machineCards.forEach(function (card, index) {
                card.style.transitionDelay = (index * 40) + "ms";
                observer.observe(card);
            });

        } else {
            // Fallback — show everything if IO unsupported
            machineCards.forEach(function (card) {
                card.classList.add("is-visible");
            });
        }


        /* -------------------------------------------------
           IMAGE FALLBACK
           If a machine image fails to load, show the
           placeholder pattern instead of a broken icon.
        ------------------------------------------------- */

        document.querySelectorAll(".machine-visual img").forEach(function (img) {
            img.addEventListener("error", function () {
                const parent = img.closest(".machine-visual");
                if (parent) {
                    parent.classList.add("no-image");
                }
                img.style.display = "none";
            });
        });


        /* -------------------------------------------------
           SMOOTH SCROLL FOR HASH LINKS
        ------------------------------------------------- */

        document.querySelectorAll('a[href^="#"]').forEach(function (link) {
            link.addEventListener("click", function (event) {
                const targetId = link.getAttribute("href");
                if (targetId === "#" || targetId.length < 2) return;

                const target = document.querySelector(targetId);
                if (!target) return;

                event.preventDefault();
                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });
            });
        });

    });
})();