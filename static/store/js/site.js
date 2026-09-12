/* =========================================================
   GITANJALI GLOBAL JAVASCRIPT
   Mobile navigation + stationery product controls
========================================================= */

(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {

        /* -------------------------------------------------
           MOBILE NAVIGATION
        ------------------------------------------------- */

        const menuButton = document.querySelector("[data-menu-toggle]");
        const mobileNav = document.querySelector("[data-mobile-nav]");

        if (menuButton && mobileNav) {
            menuButton.addEventListener("click", function () {
                const open = mobileNav.classList.toggle("open");
                menuButton.setAttribute("aria-expanded", String(open));
            });

            mobileNav.querySelectorAll("a").forEach(function (link) {
                link.addEventListener("click", function () {
                    mobileNav.classList.remove("open");
                    menuButton.setAttribute("aria-expanded", "false");
                });
            });

            document.addEventListener("keydown", function (event) {
                if (event.key === "Escape" && mobileNav.classList.contains("open")) {
                    mobileNav.classList.remove("open");
                    menuButton.setAttribute("aria-expanded", "false");
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
            showToast(productName);
            animateAdded(button);
        }

        function animateAdded(button) {
            if (!button) {
                return;
            }

            const text =
                button.querySelector("span");

            if (!text) {
                return;
            }

            const original =
                text.textContent;

            text.textContent = "Added ✓";
            button.classList.add("added");

            setTimeout(function () {
                text.textContent = original;
                button.classList.remove("added");
            }, 1400);
        }


        /* -------------------------------------------------
           FILTER PRODUCTS
        ------------------------------------------------- */

        function filterProducts() {
            let visibleCount = 0;

            productCards.forEach(function (card) {
                const category =
                    (card.dataset.category || "").toLowerCase();

                const brand =
                    (card.dataset.brand || "").toLowerCase();

                const searchData =
                    (card.dataset.search || "").toLowerCase();

                const categoryMatch =
                    activeCategory === "all" ||
                    category === activeCategory;

                const brandMatch =
                    activeBrand === "all" ||
                    brand === activeBrand;

                const searchMatch =
                    searchTerm === "" ||
                    searchData.includes(searchTerm);

                const visible =
                    categoryMatch &&
                    brandMatch &&
                    searchMatch;

                card.classList.toggle("hidden", !visible);

                if (visible) {
                    visibleCount++;
                }
            });

            if (emptyResults) {
                emptyResults.hidden = visibleCount !== 0;
            }

            updateFilterMessage();
        }


        /* -------------------------------------------------
           FILTER MESSAGE
        ------------------------------------------------- */

        function updateFilterMessage() {
            if (!activeFilterMessage) {
                return;
            }

            const parts = [];

            if (activeCategory !== "all") {
                parts.push(
                    "Category: " +
                    capitalizeWords(activeCategory)
                );
            }

            if (activeBrand !== "all") {
                parts.push(
                    "Brand: " +
                    capitalizeWords(activeBrand)
                );
            }

            if (searchTerm) {
                parts.push(
                    'Search: "' +
                    searchTerm +
                    '"'
                );
            }

            activeFilterMessage.textContent =
                parts.length
                    ? "Showing results — " + parts.join(" · ")
                    : "Showing all products";
        }


        /* -------------------------------------------------
           CATEGORY FILTER
        ------------------------------------------------- */

        filterButtons.forEach(function (button) {
            button.addEventListener("click", function () {

                activeCategory =
                    (button.dataset.filter || "all").toLowerCase();

                filterButtons.forEach(function (item) {
                    item.classList.toggle(
                        "active",
                        item === button
                    );
                });

                filterProducts();
            });
        });


        /* -------------------------------------------------
           BRAND FILTER
        ------------------------------------------------- */

        brandButtons.forEach(function (button) {
            button.addEventListener("click", function () {

                const selectedBrand =
                    (button.dataset.brand || "all").toLowerCase();

                if (activeBrand === selectedBrand) {
                    activeBrand = "all";

                    button.classList.remove("selected");

                } else {
                    activeBrand = selectedBrand;

                    brandButtons.forEach(function (item) {
                        item.classList.remove("selected");
                    });

                    button.classList.add("selected");
                }

                filterProducts();
                scrollToProducts();
            });
        });


        /* -------------------------------------------------
           SEARCH
        ------------------------------------------------- */

        if (searchInput) {
            searchInput.addEventListener("input", function () {

                searchTerm =
                    searchInput.value.trim().toLowerCase();

                if (clearSearch) {
                    clearSearch.classList.toggle(
                        "visible",
                        searchTerm.length > 0
                    );
                }

                filterProducts();
            });
        }


        /* -------------------------------------------------
           CLEAR SEARCH
        ------------------------------------------------- */

        if (clearSearch) {
            clearSearch.addEventListener("click", function () {

                if (searchInput) {
                    searchInput.value = "";
                    searchInput.focus();
                }

                searchTerm = "";
                clearSearch.classList.remove("visible");

                filterProducts();
            });
        }


        /* -------------------------------------------------
           RESET
        ------------------------------------------------- */

        function resetFilters() {
            activeCategory = "all";
            activeBrand = "all";
            searchTerm = "";

            if (searchInput) {
                searchInput.value = "";
            }

            if (clearSearch) {
                clearSearch.classList.remove("visible");
            }

            filterButtons.forEach(function (button) {
                button.classList.toggle(
                    "active",
                    (button.dataset.filter || "").toLowerCase() === "all"
                );
            });

            brandButtons.forEach(function (button) {
                button.classList.remove("selected");
            });

            filterProducts();
        }

        if (resetButton) {
            resetButton.addEventListener("click", resetFilters);
        }

        if (emptyReset) {
            emptyReset.addEventListener("click", resetFilters);
        }


        /* -------------------------------------------------
           ADD-TO-REQUEST BUTTONS
        ------------------------------------------------- */

        addButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                addProduct(button);
            });
        });


        /* -------------------------------------------------
           IMAGE FALLBACK
        ------------------------------------------------- */

        document.querySelectorAll(".product-image").forEach(function (image) {
            image.addEventListener("error", function () {

                image.style.display = "none";

                const fallback =
                    image.parentElement.querySelector(".image-fallback");

                if (fallback) {
                    fallback.style.display = "flex";
                }
            });
        });


        /* -------------------------------------------------
           SCROLL
        ------------------------------------------------- */

        function scrollToProducts() {
            const products =
                document.getElementById("products");

            if (!products) {
                return;
            }

            setTimeout(function () {
                products.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });
            }, 100);
        }


        /* -------------------------------------------------
           HELPERS
        ------------------------------------------------- */

        function capitalizeWords(value) {
            return value
                .split(" ")
                .map(function (word) {
                    return word.charAt(0).toUpperCase() +
                        word.slice(1);
                })
                .join(" ");
        }


        /* -------------------------------------------------
           INITIALIZE
        ------------------------------------------------- */

        updateRequestCounter();
        filterProducts();


        /* -------------------------------------------------
           PRODUCT REVEAL
        ------------------------------------------------- */

        if ("IntersectionObserver" in window) {

            const observer =
                new IntersectionObserver(
                    function (entries) {

                        entries.forEach(function (entry) {

                            if (entry.isIntersecting) {

                                entry.target.classList.add(
                                    "product-visible"
                                );

                                observer.unobserve(entry.target);
                            }
                        });

                    },
                    {
                        threshold: .08
                    }
                );

            productCards.forEach(function (card) {
                card.classList.add("product-reveal");
                observer.observe(card);
            });
        }
    });
})();
