/* =========================================================
   GITANJALI GLOBAL JAVASCRIPT
   Mobile navigation + stationery product controls
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
                header.classList.toggle("is-scrolled", window.scrollY > 12);
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
           IMPORTANT: this runs independently of product code.
        ------------------------------------------------- */
        const menuButton = document.querySelector("[data-menu-toggle]");
        const mobileNav = document.querySelector("[data-mobile-nav]");

        if (menuButton && mobileNav) {
            function openMenu() {
                mobileNav.classList.add("open");
                menuButton.setAttribute("aria-expanded", "true");
                mobileNav.setAttribute("aria-hidden", "false");
            }

            function closeMenu() {
                mobileNav.classList.remove("open");
                menuButton.setAttribute("aria-expanded", "false");
                mobileNav.setAttribute("aria-hidden", "true");
            }

            function toggleMenu(event) {
                if (event) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                if (mobileNav.classList.contains("open")) {
                    closeMenu();
                } else {
                    openMenu();
                }
            }

            mobileNav.setAttribute("aria-hidden", "true");

            // Use click only. Do NOT prevent pointerup: on some phones that
            // suppresses the synthetic click event and makes the button appear dead.
            menuButton.addEventListener("click", toggleMenu, false);

            mobileNav.querySelectorAll("a").forEach(function (link) {
                link.addEventListener("click", closeMenu, false);
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
           The navigation above must never depend on these.
        ------------------------------------------------- */
        const productCards = Array.from(document.querySelectorAll(".product-card"));

        if (!productCards.length) {
            return;
        }

        const searchInput = document.getElementById("product-search");
        const clearSearch = document.getElementById("clear-search");
        const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));
        const brandButtons = Array.from(document.querySelectorAll("[data-brand]"));
        const resetButton = document.getElementById("reset-filters");
        const emptyReset = document.getElementById("empty-reset");
        const emptyResults = document.getElementById("empty-results");
        const activeFilterMessage = document.getElementById("active-filter-message");
        const toast = document.getElementById("stationery-toast");
        const toastProduct = document.querySelector("[data-toast-product]");
        const requestCounters = document.querySelectorAll("[data-request-count]");
        const addButtons = document.querySelectorAll("[data-add-product]");

        const STORAGE_KEY = "gitanjali_request_items";
        let activeCategory = "all";
        let activeBrand = "all";
        let searchTerm = "";
        let requestItems = loadRequestItems();
        let toastTimer = null;

        function loadRequestItems() {
            try {
                const saved = localStorage.getItem(STORAGE_KEY);
                if (!saved) return [];
                const parsed = JSON.parse(saved);
                return Array.isArray(parsed) ? parsed : [];
            } catch (error) {
                console.warn("Could not load request items.", error);
                return [];
            }
        }

        function saveRequestItems() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(requestItems));
            } catch (error) {
                console.warn("Could not save request items.", error);
            }
        }

        function updateRequestCounter() {
            requestCounters.forEach(function (counter) {
                counter.textContent = requestItems.length;
            });
        }

        function showToast(productName) {
            if (!toast) return;

            if (toastProduct) {
                toastProduct.textContent = productName;
            }

            toast.classList.add("show");
            clearTimeout(toastTimer);
            toastTimer = setTimeout(function () {
                toast.classList.remove("show");
            }, 2600);
        }

        function addProduct(button) {
            const productName = button.dataset.product || "Product";
            const brand = button.dataset.brand || "";

            const existing = requestItems.find(function (item) {
                return item.name === productName;
            });

            if (!existing) {
                requestItems.push({ name: productName, brand: brand });
                saveRequestItems();
            }

            updateRequestCounter();
            showToast(productName);
        }

        addButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                addProduct(button);
            });
        });

        function applyProductFilters() {
            let visibleCount = 0;

            productCards.forEach(function (card) {
                const category = (card.dataset.category || "").toLowerCase();
                const brand = (card.dataset.brand || "").toLowerCase();
                const searchable = (card.dataset.search || card.dataset.name || "").toLowerCase();

                const categoryOK = activeCategory === "all" || category === activeCategory;
                const brandOK = activeBrand === "all" || brand === activeBrand;
                const searchOK = !searchTerm || searchable.includes(searchTerm);
                const visible = categoryOK && brandOK && searchOK;

                card.hidden = !visible;
                if (visible) visibleCount += 1;
            });

            if (emptyResults) {
                emptyResults.hidden = visibleCount !== 0;
            }

            if (activeFilterMessage) {
                activeFilterMessage.textContent = visibleCount + " product" +
                    (visibleCount === 1 ? "" : "s") + " shown.";
            }
        }

        filterButtons.forEach(function (button) {
            button.addEventListener("click", function (event) {
                event.preventDefault();
                activeCategory = (button.dataset.filter || "all").toLowerCase();
                filterButtons.forEach(function (item) {
                    item.classList.toggle("active", item === button);
                });
                applyProductFilters();
            });
        });

        brandButtons.forEach(function (button) {
            button.addEventListener("click", function (event) {
                if (!button.dataset.brand) return;
                event.preventDefault();
                activeBrand = button.dataset.brand.toLowerCase();
                brandButtons.forEach(function (item) {
                    item.classList.toggle("active", item === button);
                });
                applyProductFilters();
            });
        });

        if (searchInput) {
            searchInput.addEventListener("input", function () {
                searchTerm = searchInput.value.trim().toLowerCase();
                applyProductFilters();
            });
        }

        if (clearSearch) {
            clearSearch.addEventListener("click", function () {
                if (searchInput) {
                    searchInput.value = "";
                    searchTerm = "";
                    applyProductFilters();
                    searchInput.focus();
                }
            });
        }

        function resetFilters(event) {
            if (event) event.preventDefault();
            activeCategory = "all";
            activeBrand = "all";
            searchTerm = "";

            if (searchInput) searchInput.value = "";
            filterButtons.forEach(function (button) {
                button.classList.toggle("active", (button.dataset.filter || "all") === "all");
            });
            brandButtons.forEach(function (button) {
                button.classList.remove("active");
            });
            applyProductFilters();
        }

        if (resetButton) resetButton.addEventListener("click", resetFilters);
        if (emptyReset) emptyReset.addEventListener("click", resetFilters);

        updateRequestCounter();
    });
})();
