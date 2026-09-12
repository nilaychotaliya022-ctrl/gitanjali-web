from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from urllib.parse import quote

from .forms import QuoteForm, ReviewForm
from .models import Review


PRODUCTS = [

    # =========================
    # SCHOOL STATIONERY
    # =========================
    {
        "category": "School",
        "name": "School Notebook",
        "brand": "Classmate",
        "copy": "Quality notebooks for everyday school notes, homework, and classwork.",
        "image": "/static/store/images/classmate_notebook.jpg",
    },
    {
        "category": "School",
        "name": "Geometry Box",
        "brand": "DOMS",
        "copy": "Complete geometry essentials for school mathematics and technical drawing.",
        "image": "/static/store/images/geometry.jpg",
    },
    {
        "category": "School",
        "name": "School Writing Kit",
        "brand": "DOMS",
        "copy": "Pens, pencils, erasers, sharpeners and everyday writing essentials.",
        "image": "/static/store/images/WRITINGKIT.jpg",
    },
    {
        "category": "School",
        "name": "Colour Pencil Set",
        "brand": "DOMS",
        "copy": "Bright and smooth colour pencils for school projects and creative work.",
        "image": "/static/store/images/COLORKIT.jpg",
    },

    # =========================
    # OFFICE STATIONERY
    # =========================
    {
        "category": "Office",
        "name": "Office Writing Essentials",
        "brand": "Cello",
        "copy": "Reliable pens and writing tools for reception desks, offices and daily work.",
        "image": "/static/store/images/officekit.jpg",
    },
    {
        "category": "Office",
        "name": "Premium Office Notebook",
        "brand": "Classmate",
        "copy": "Professional notebooks for meetings, planning, records and daily notes.",
        "image": "/static/store/images/classmetnot.jpg",
    },
    {
        "category": "Office",
        "name": "Office Desk Essentials",
        "brand": "Kangaro",
        "copy": "Staplers, punches, clips and useful tools for a productive office desk.",
        "image": "/static/store/images/kangaroo.jpg",
    },

    # =========================
    # BILL BOOKS
    # =========================
    {
        "category": "Bill Books",
        "name": "Duplicate Bill Book",
        "brand": "Gitanjali",
        "copy": "Practical duplicate bill books for shops, businesses and daily transactions.",
        "image": "/static/store/images/billbook.jpg",
    },
    {
        "category": "Bill Books",
        "name": "Triplicate Bill Book",
        "brand": "Gitanjali",
        "copy": "Three-copy bill books designed for organised business record keeping.",
        "image": "/static/store/images/triplicate.jpg",
    },
    {
        "category": "Bill Books",
        "name": "Cash Memo Book",
        "brand": "Gitanjali",
        "copy": "Easy-to-use cash memo books for retail counters and businesses.",
        "image": "/static/store/images/cashmemo.jpg",
    },

    # =========================
    # ACCOUNT BOOKS
    # =========================
    {
        "category": "Accounts",
        "name": "Register",
        "brand": "Gitanjali",
        "copy": "Ruled account books for ledgers, customer records and business accounts.",
        "image": "/static/store/images/register.jpg",
    },
    {
        "category": "Accounts",
        "name": "Spiral Diary",
        "brand": "Gitanjali",
        "copy": "Keep daily cash transactions and financial records organised.",
        "image": "/static/store/images/diary.jpg",
    },
    {
        "category": "Accounts",
        "name": "Office Diary",
        "brand": "Gitanjali",
        "copy": "Useful ledger books for shops, offices and professional record keeping.",
        "image": "/static/store/images/diary2.jpg",
    },

    # =========================
    # FILES
    # =========================
    {
        "category": "Files",
        "name": "Document Files",
        "brand": "Gitanjali",
        "copy": "Keep important documents protected, organised and easy to find.",
        "image": "/static/store/images/docfile.jpg",
    },
    {
        "category": "Files",
        "name": "Office Folder",
        "brand": "Gitanjali",
        "copy": "Professional folders for reports, documents and office paperwork.",
        "image": "/static/store/images/folder.jpg",
    },
    {
        "category": "Files",
        "name": "Plastic File Folder",
        "brand": "Gitanjali",
        "copy": "Lightweight document storage for school, office and personal use.",
        "image": "/static/store/images/plastic.jpg",
    },

    # =========================
    # OFFICE SUPPLIES
    # =========================
    {
        "category": "Office Supplies",
        "name": "Stapler",
        "brand": "Kangaro",
        "copy": "Strong and dependable staplers for everyday office paperwork.",
        "image": "/static/store/images/stepler.jpg",
    },
    {
        "category": "Office Supplies",
        "name": "Paper Punch",
        "brand": "Kangaro",
        "copy": "Precision paper punches for organised filing and document preparation.",
        "image": "/static/store/images/punch.jpg",
    },
    {
        "category": "Office Supplies",
        "name": "Adhesive Tape",
        "brand": "Pidilite",
        "copy": "Useful adhesive solutions for packaging, office work and everyday tasks.",
        "image": "/static/store/images/tap.jpg",
    },

    # =========================
    # WRITING
    # =========================
    {
        "category": "Writing",
        "name": "Gel Pens",
        "brand": "Cello",
        "copy": "Smooth-flowing pens designed for comfortable everyday writing.",
        "image": "/static/store/images/gelpen.jpg",
    },
    {
        "category": "Writing",
        "name": "Permanent Marker",
        "brand": "Artline",
        "copy": "Bold permanent markers for labels, packaging, boards and general use.",
        "image": "/static/store/images/marker.jpg",
    },
    {
        "category": "Writing",
        "name": "Whiteboard Marker",
        "brand": "Artline",
        "copy": "Clear, easy-to-read markers for classrooms, offices and presentations.",
        "image": "/static/store/images/whitemarker.jpg",
    },

    # =========================
    # PAPER
    # =========================
    {
        "category": "Paper",
        "name": "A4 Copier Paper",
        "brand": "Paper",
        "copy": "Reliable everyday paper for printing, copying, documentation and office work.",
        "image": "/static/store/images/paper.jpg",
    },
    {
        "category": "Paper",
        "name": "Colour Paper",
        "brand": "Paper",
        "copy": "Colourful paper for school projects, office presentations and creative work.",
        "image": "/static/store/images/colorpaper.jpg",
    },

    # =========================
    # ART & CRAFT
    # =========================
    {
        "category": "Art & Craft",
        "name": "Art Colour Set",
        "brand": "DOMS",
        "copy": "Creative colour supplies for students, artists and craft projects.",
        "image": "/static/store/images/artcolorset.jpg",
    },
    {
        "category": "Art & Craft",
        "name": "Craft Adhesive",
        "brand": "Pidilite",
        "copy": "Trusted adhesive for school projects, crafts and everyday creative work.",
        "image": "/static/store/images/craft.jpg",
    },

]


STAMP_TYPES = [
    ("Office seal", "For documents that need your official mark.", "from ₹280", "briefcase"),
    ("Address stamp", "A neat return address for every envelope.", "from ₹240", "pin"),
    ("Date & received", "For logs, inward desks, and well-kept records.", "from ₹320", "clock"),
    ("Name / signature", "A personal mark for books, parcels, and gifts.", "from ₹260", "pen"),
]


def shared_context(**extra):
    return {
        "nav_items": [
            ("home", "Home", "/"),
            ("stationery", "Stationery", "/stationery/"),
            ("printing", "Printing", "/printing/"),
            ("stamps", "Rubber stamps", "/rubber-stamps/"),
            ("about", "Our story", "/about/"),
        ],
        **extra,
    }


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


def stationery(request):
    categories = sorted(
        set(product["category"] for product in PRODUCTS)
    )

    brands = sorted(
        set(product["brand"] for product in PRODUCTS)
    )

    return render(
        request,
        "store/stationery.html",
        shared_context(
            active="stationery",
            products=PRODUCTS,
            categories=categories,
            brands=brands,
        ),
    )


def printing(request):
    return render(
        request,
        "store/printing.html",
        shared_context(
            active="printing",
            quote_form=QuoteForm(initial={"service": "printing"}),
        ),
    )


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
