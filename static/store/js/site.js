/* =========================================================
   GITANJALI GLOBAL JAVASCRIPT
   Mobile navigation + stationery product controls
   Enhanced with scroll effects and animations
========================================================= */

(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {

        /* -------------------------------------------------
           HEADER SCROLL EFFECT
        ------------------------------------------------- */

        const header = document.querySelector("[data-header]");

        if (header) {
            let ticking = false;

            function updateHeader() {
                const scrolled = window.scrollY > 12;

                header.classList.toggle("is-scrolled", scrolled);
                ticking = false;
            }

            window.addEventListener("scroll", function () {
                if (!ticking) {
                    window.requestAnimationFrame(updateHeader);
                    ticking = true;
                }
            }, { passive: true });

            updateHeader();
        }


        /* -------------------------------------------------
           MOBILE NAVIGATION
        ------------------------------------------------- */

        const menuButton = document.querySelector("[data-menu-toggle]");
        const mobileNav = document.querySelector("[data-mobile-nav]");

        if (menuButton && mobileNav) {

            function closeMenu() {
                mobileNav.classList.remove("open");
                menuButton.setAttribute("aria-expanded", "false");
            }

            menuButton.addEventListener("click", function () {
                const open = mobileNav.classList.toggle("open");
                menuButton.setAttribute("aria-expanded", String(open));
            });

            mobileNav.querySelectorAll("a").forEach(function (link) {
                link.addEventListener("click", closeMenu);
            });

            document.addEventListener("keydown", function (event) {
                if (event.key === "Escape" && mobileNav.classList.contains("open")) {
                    closeMenu();
                    menuButton.focus();
                }
            });

            document.addEventListener("click", function (event) {
                if (
                    mobileNav.classList.contains("open") &&
                    !mobileNav.contains(event.target) &&
                    !menuButton.contains(event.target)
                ) {
                    closeMenu();
                }
            });
        }


        /* -------------------------------------------------
           STATIONERY PRODUCT CONTROLS
        ------------------------------------------------- */

        const productCards = Array.from(
            document.querySelectorAll(".product-card")
        );

        if (!productCards.length) {
            return;
        }

        const searchInput = document.getElementById("product-search");
        const clearSearch = document.getElementById("clear-search");

        const filterButtons = Array.from(
            document.querySelectorAll("[data-filter]")
        );

        const brandButtons = Array.from(
            document.querySelectorAll("[data-brand]")
        );

        const resetButton = document.getElementById("reset-filters");
        const emptyReset = document.getElementById("empty-reset");
        const emptyResults = document.getElementById("empty-results");
        const activeFilterMessage =
            document.getElementById("active-filter-message");

        const toast = document.getElementById("stationery-toast");
        const toastProduct = document.querySelector("[data-toast-product]");

        const requestCounters =
            document.querySelectorAll("[data-request-count]");

        const addButtons =
            document.querySelectorAll("[data-add-product]");

        const STORAGE_KEY = "gitanjali_request_items";

        let activeCategory = "all";
        let activeBrand = "all";
        let searchTerm = "";
        let requestItems = loadRequestItems();
        let toastTimer = null;


        /* -------------------------------------------------
           LOCAL STORAGE
        ------------------------------------------------- */

        function loadRequestItems() {
            try {
                const saved = localStorage.getItem(STORAGE_KEY);

                if (!saved) {
                    return [];
                }

                const parsed = JSON.parse(saved);

                return Array.isArray(parsed) ? parsed : [];

            } catch (error) {
                console.warn("Could not load request items.", error);
                return [];
            }
        }

        function saveRequestItems() {
            try {
                localStorage.setItem(
                    STORAGE_KEY,
                    JSON.stringify(requestItems)
                );
            } catch (error) {
                console.warn("Could not save request items.", error);
            }
        }


        /* -------------------------------------------------
           REQUEST COUNTER
        ------------------------------------------------- */

        function updateRequestCounter() {
            requestCounters.forEach(function (counter) {
                counter.textContent = requestItems.length;
            });
        }


        /* -------------------------------------------------
           TOAST
        ------------------------------------------------- */

        function showToast(productName) {
            if (!toast) {
                return;
            }

            if (toastProduct) {
                toastProduct.textContent = productName;
            }

            toast.classList.add("show");

            clearTimeout(toastTimer);

            toastTimer = setTimeout(function () {
                toast.classList.remove("show");
            }, 2600);
        }


        /* -------------------------------------------------
           ADD PRODUCT
        ------------------------------------------------- */

        function addProduct(button) {
            const productName =
                button.dataset.product || "Product";

            const brand =
                button.dataset.brand || "";

            const existing =
                requestItems.find(function (item) {
                    return item.name === productName;
                });

            if (!existing) {
                requestItems.push({
                    name: productName,
                    brand: brand
                });

                saveRequestItems();
            }

            updateRequestCounter();
            showToast