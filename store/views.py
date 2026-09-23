from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from urllib.parse import quote

from .forms import QuoteForm, ReviewForm
from .models import Review, Category, Product


# =========================================================
# STATIC — stamp types
# =========================================================

STAMP_TYPES = [
    ("Office seal", "For documents that need your official mark.", "from ₹280", "briefcase"),
    ("Address stamp", "A neat return address for every envelope.", "from ₹240", "pin"),
    ("Date & received", "For logs, inward desks, and well-kept records.", "from ₹320", "clock"),
    ("Name / signature", "A personal mark for books, parcels, and gifts.", "from ₹260", "pen"),
]


def shared_context(**extra):
    return {
        "nav_items": [
            ("home",         "Home",           "/"),
            ("stationery",   "Stationery",     "/stationery/"),
            ("all_products", "All products",   "/products/"),
            ("printing",     "Printing",       "/printing/"),
            ("stamps",       "Rubber stamps",  "/rubber-stamps/"),
            ("about",        "Our story",      "/about/"),
        ],
        **extra,
    }


# =========================================================
# HOME
# =========================================================

def home(request):
    review_form = ReviewForm(request.POST or None)

    if request.method == "POST" and review_form.is_valid():
        review_form.save()
        messages.success(request, "Thanks — your review is now live.")
        return redirect("home")

    return render(
        request,
        "store/home.html",
        shared_context(
            active="home",
            reviews=Review.objects.all(),
            review_form=review_form,
        ),
    )


# =========================================================
# STATIONERY (categorised, PAGINATED)
# =========================================================

def stationery(request):
    """
    Stationery page — shows category tiles + brands,
    and a paginated grid of products (12 per page).
    Supports search (?q=) and category filter (?cat=).
    """
    q = (request.GET.get("q") or "").strip()
    cat_slug = (request.GET.get("cat") or "").strip()

    categories = Category.objects.all().prefetch_related("products")

    products_qs = (
        Product.objects
        .filter(is_active=True)
        .select_related("category")
    )

    # Category filter
    if cat_slug and cat_slug != "all":
        products_qs = products_qs.filter(category__slug=cat_slug)

    # Search
    if q:
        from django.db.models import Q
        products_qs = products_qs.filter(
            Q(name__icontains=q)
            | Q(brand__icontains=q)
            | Q(copy__icontains=q)
            | Q(category__name__icontains=q)
        )

    # Brands (from active products)
    brands = sorted(
        {p.brand for p in Product.objects.filter(is_active=True) if p.brand}
    )

    # Paginate — 12 per page
    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "store/stationery.html",
        shared_context(
            active="stationery",
            categories=categories,
            brands=brands,
            page_obj=page_obj,
            products=page_obj.object_list,
            total_products=paginator.count,
            q=q,
            active_category=cat_slug,
        ),
    )


# =========================================================
# ALL PRODUCTS (flat list, PAGINATED)
# =========================================================

def all_products(request):
    """
    A flat, paginated listing of every active product.
    Supports search (?q=) and category filter (?cat=).
    """
    q = (request.GET.get("q") or "").strip()
    cat_slug = (request.GET.get("cat") or "").strip()

    categories = Category.objects.all()

    products_qs = (
        Product.objects
        .filter(is_active=True)
        .select_related("category")
    )

    if cat_slug and cat_slug != "all":
        products_qs = products_qs.filter(category__slug=cat_slug)

    if q:
        from django.db.models import Q
        products_qs = products_qs.filter(
            Q(name__icontains=q)
            | Q(brand__icontains=q)
            | Q(copy__icontains=q)
            | Q(category__name__icontains=q)
        )

    brands = sorted(
        {p.brand for p in Product.objects.filter(is_active=True) if p.brand}
    )

    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "store/all_products.html",
        shared_context(
            active="all_products",
            categories=categories,
            brands=brands,
            page_obj=page_obj,
            products=page_obj.object_list,
            total_products=paginator.count,
            q=q,
            active_category=cat_slug,
        ),
    )


# =========================================================
# PRINTING
# =========================================================

def printing(request):
    return render(
        request,
        "store/printing.html",
        shared_context(
            active="printing",
            quote_form=QuoteForm(initial={"service": "printing"}),
        ),
    )


# =========================================================
# RUBBER STAMPS
# =========================================================

def rubber_stamps(request):
    return render(
        request,
        "store/rubber_stamps.html",
        shared_context(
            active="stamps",
            stamp_types=STAMP_TYPES,
            quote_form=QuoteForm(),
        ),
    )


# =========================================================
# ABOUT
# =========================================================

def about(request):
    review_form = ReviewForm(request.POST or None)

    if request.method == "POST" and review_form.is_valid():
        review_form.save()
        messages.success(request, "Thanks — your review is now live.")
        return redirect("about")

    return render(
        request,
        "store/about.html",
        shared_context(
            active="about",
            reviews=Review.objects.all(),
            review_form=review_form,
        ),
    )


# =========================================================
# CONTACT
# =========================================================

def contact(request):
    form = QuoteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        whatsapp_number = "919409734116"
        service = data.get("service") or "Not specified"
        deadline = data.get("deadline") or "Not specified"
        details = data.get("details") or "No additional details"

        whatsapp_message = (
            "Hello Gitanjali Stationery & Rubber Stamp!\n\n"
            f"Name: {data['name']}\n"
            f"Phone: {data['phone']}\n"
            f"Service: {service}\n"
            f"Needed by: {deadline}\n"
            f"Message: {details}"
        )

        whatsapp_url = (
            f"https://wa.me/{whatsapp_number}?text={quote(whatsapp_message)}"
        )

        return HttpResponseRedirect(whatsapp_url)

    return render(
        request,
        "store/contact.html",
        shared_context(
            active="contact",
            form=form,
        ),
    )