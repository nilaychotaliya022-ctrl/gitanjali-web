/* =========================================================
   GITANJALI — STATIONERY PAGE JS
   Handles: search, category filter, brand filter,
            request list, toast, empty state
========================================================= */

(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {

    // ---------- ELEMENTS ----------
    const searchInput   = document.getElementById("product-search");
    const clearSearch   = document.getElementById("clear-search");
    const resetFilters  = document.getElementById("reset-filters");
    const emptyReset    = document.getElementById("empty-reset");
    const emptyResults  = document.getElementById("empty-results");
    const filterMsg     = document.getElementById("active-filter-message");

    const categoryChips = document.querySelectorAll(".filter-chip[data-filter]");
    const brandCards    = document.querySelectorAll(".brand-card[data-brand]");
    const categoryTiles = document.querySelectorAll(".category-tile[data-category]");
    const productCards  = document.querySelectorAll(".product-card");

    const requestCountEl  = document.querySelector("[data-request-count]");
    const toast           = document.getElementById("stationery-toast");
    const toastProductEl  = document.querySelector("[data-toast-product]");

    // ---------- STATE ----------
    let activeCategory = "all";
    let activeBrand    = "";
    let searchTerm     = "";
    let requestList    = [];

    // ---------- FILTER LOGIC ----------
    function applyFilters() {
      let visible = 0;

      productCards.forEach(function (card) {
        const cat   = (card.dataset.category || "").toLowerCase();
        const brand = (card.dataset.brand    || "").toLowerCase();
        const hay   = (card.dataset.search   || "").toLowerCase();

        const matchesCategory =
          activeCategory === "all" || cat === activeCategory;

        const matchesBrand =
          !activeBrand || brand === activeBrand;

        const matchesSearch =
          !searchTerm || hay.indexOf(searchTerm) !== -1;

        const show = matchesCategory && matchesBrand && matchesSearch;

        card.classList.toggle("hidden", !show);
        if (show) visible++;
      });

      // empty state
      if (emptyResults) {
        emptyResults.hidden = !(visible === 0 && productCards.length > 0);
      }

      // message
      if (filterMsg) {
        const parts = [];
        if (activeCategory !== "all") {
          const chip = document.querySelector(
            '.filter-chip[data-filter="' + activeCategory + '"]'
          );
          if (chip) parts.push('category "' + chip.textContent.trim() + '"');
        }
        if (activeBrand) {
          parts.push('brand "' + activeBrand + '"');
        }
        if (searchTerm) {
          parts.push('search "' + searchTerm + '"');
        }

        if (parts.length === 0) {
          filterMsg.textContent = "Showing all products";
        } else if (visible === 0) {
          filterMsg.textContent = "No products match " + parts.join(" and ") + ".";
        } else {
          filterMsg.textContent =
            "Showing " + visible + " product" + (visible === 1 ? "" : "s") +
            " for " + parts.join(" and ") + ".";
        }
      }
    }

    // ---------- SEARCH ----------
    if (searchInput) {
      searchInput.addEventListener("input", function (e) {
        searchTerm = e.target.value.trim().toLowerCase();
        if (clearSearch) {
          clearSearch.classList.toggle("visible", searchTerm.length > 0);
        }
        applyFilters();
      });
    }

    if (clearSearch) {
      clearSearch.addEventListener("click", function () {
        if (searchInput) searchInput.value = "";
        searchTerm = "";
        clearSearch.classList.remove("visible");
        applyFilters();
      });
    }

    // ---------- CATEGORY CHIPS ----------
    categoryChips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        categoryChips.forEach(function (c) { c.classList.remove("active"); });
        chip.classList.add("active");
        activeCategory = (chip.dataset.filter || "all").toLowerCase();

        // Scroll to products grid
        const grid = document.getElementById("products");
        if (grid) grid.scrollIntoView({ behavior: "smooth", block: "start" });

        applyFilters();
      });
    });

    // ---------- BRAND CARDS ----------
    brandCards.forEach(function (card) {
      card.addEventListener("click", function () {
        const brand = (card.dataset.brand || "").toLowerCase();

        if (activeBrand === brand) {
          activeBrand = "";
          card.classList.remove("selected");
        } else {
          brandCards.forEach(function (c) { c.classList.remove("selected"); });
          activeBrand = brand;
          card.classList.add("selected");
        }

        const grid = document.getElementById("products");
        if (grid) grid.scrollIntoView({ behavior: "smooth", block: "start" });

        applyFilters();
      });
    });

    // ---------- CATEGORY TILES ----------
    categoryTiles.forEach(function (tile) {
      tile.addEventListener("click", function () {
        const cat = (tile.dataset.category || "all").toLowerCase();
        activeCategory = cat;

        categoryChips.forEach(function (c) {
          c.classList.toggle("active", (c.dataset.filter || "").toLowerCase() === cat);
        });

        const grid = document.getElementById("products");
        if (grid) grid.scrollIntoView({ behavior: "smooth", block: "start" });

        applyFilters();
      });
    });

    // ---------- RESET ----------
    function resetAll() {
      activeCategory = "all";
      activeBrand    = "";
      searchTerm     = "";

      if (searchInput) searchInput.value = "";
      if (clearSearch) clearSearch.classList.remove("visible");

      categoryChips.forEach(function (c) {
        c.classList.toggle("active", (c.dataset.filter || "") === "all");
      });

      brandCards.forEach(function (c) { c.classList.remove("selected"); });

      applyFilters();
    }

    if (resetFilters) resetFilters.addEventListener("click", resetAll);
    if (emptyReset)   emptyReset.addEventListener("click", resetAll);

    // ---------- REQUEST LIST ----------
    function updateRequestCount() {
      if (requestCountEl) requestCountEl.textContent = requestList.length;
    }

    function showToast(name) {
      if (!toast) return;
      if (toastProductEl) toastProductEl.textContent = name;
      toast.classList.add("show");
      clearTimeout(showToast._t);
      showToast._t = setTimeout(function () {
        toast.classList.remove("show");
      }, 2400);
    }

    function addToRequest(name, btn) {
      if (!name) return;
      if (requestList.indexOf(name) === -1) {
        requestList.push(name);
      }
      updateRequestCount();

      if (btn) {
        btn.classList.add("added");
        const label = btn.querySelector("span");
        if (label) {
          const original = label.textContent;
          label.textContent = "Added ✓";
          setTimeout(function () {
            btn.classList.remove("added");
            label.textContent = original;
          }, 1800);
        }
      }

      showToast(name);
    }

    document.querySelectorAll("[data-add-product]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        addToRequest(btn.dataset.product || btn.dataset.addProduct, btn);
      });
    });

    // ---------- INITIALISE ----------
    applyFilters();

  });

})();