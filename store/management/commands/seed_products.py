from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File

from store.models import Category, Product


CATEGORIES = [
    {"slug": "art-craft",         "name": "Art & Craft",       "icon": "✎", "blurb": "Colours, brushes, adhesives and creative supplies."},
    {"slug": "office-stationery", "name": "Office Stationery", "icon": "⌨", "blurb": "Everyday writing, desk tools and essentials for offices."},
    {"slug": "school-stationery", "name": "School Stationery", "icon": "✏", "blurb": "Notebooks, geometry sets and learning supplies for students."},
    {"slug": "office-accounts",   "name": "Office Accounts",   "icon": "▤", "blurb": "Registers, bill books, diaries and account-keeping essentials."},
    {"slug": "papers",            "name": "Papers",            "icon": "▦", "blurb": "A4, colour and specialty paper for printing and offices."},
    {"slug": "supplies",          "name": "Supplies",          "icon": "⚙", "blurb": "Staplers, punches, tapes, files and general office supplies."},
]


PRODUCTS = [
    # School Stationery
    {"category_slug": "school-stationery", "name": "School Notebook",    "brand": "Classmate", "copy": "Quality notebooks for everyday school notes, homework, and classwork.", "image": "classmate_notebook.jpg"},
    {"category_slug": "school-stationery", "name": "Geometry Box",       "brand": "DOMS",      "copy": "Complete geometry essentials for school mathematics and technical drawing.", "image": "geometry.jpg"},
    {"category_slug": "school-stationery", "name": "School Writing Kit", "brand": "DOMS",      "copy": "Pens, pencils, erasers, sharpeners and everyday writing essentials.", "image": "WRITINGKIT.jpg"},
    {"category_slug": "school-stationery", "name": "Colour Pencil Set",  "brand": "DOMS",      "copy": "Bright and smooth colour pencils for school projects and creative work.", "image": "COLORKIT.jpg"},

    # Office Stationery
    {"category_slug": "office-stationery", "name": "Office Writing Essentials", "brand": "Cello",     "copy": "Reliable pens and writing tools for reception desks, offices and daily work.", "image": "officekit.jpg"},
    {"category_slug": "office-stationery", "name": "Premium Office Notebook",   "brand": "Classmate", "copy": "Professional notebooks for meetings, planning, records and daily notes.", "image": "classmetnot.jpg"},
    {"category_slug": "office-stationery", "name": "Office Desk Essentials",    "brand": "Kangaro",   "copy": "Staplers, punches, clips and useful tools for a productive office desk.", "image": "kangaroo.jpg"},

    # Office Accounts
    {"category_slug": "office-accounts", "name": "Duplicate Bill Book",  "brand": "Gitanjali", "copy": "Practical duplicate bill books for shops, businesses and daily transactions.", "image": "billbook.jpg"},
    {"category_slug": "office-accounts", "name": "Triplicate Bill Book", "brand": "Gitanjali", "copy": "Three-copy bill books designed for organised business record keeping.", "image": "triplicate.jpg"},
    {"category_slug": "office-accounts", "name": "Cash Memo Book",       "brand": "Gitanjali", "copy": "Easy-to-use cash memo books for retail counters and businesses.", "image": "cashmemo.jpg"},
    {"category_slug": "office-accounts", "name": "Register",             "brand": "Gitanjali", "copy": "Ruled account books for ledgers, customer records and business accounts.", "image": "register.jpg"},
    {"category_slug": "office-accounts", "name": "Spiral Diary",         "brand": "Gitanjali", "copy": "Keep daily cash transactions and financial records organised.", "image": "diary.jpg"},
    {"category_slug": "office-accounts", "name": "Office Diary",         "brand": "Gitanjali", "copy": "Useful ledger books for shops, offices and professional record keeping.", "image": "diary2.jpg"},

    # Papers
    {"category_slug": "papers", "name": "Document Files",      "brand": "Gitanjali", "copy": "Keep important documents protected, organised and easy to find.", "image": "docfile.jpg"},
    {"category_slug": "papers", "name": "Office Folder",       "brand": "Gitanjali", "copy": "Professional folders for reports, documents and office paperwork.", "image": "folder.jpg"},
    {"category_slug": "papers", "name": "Plastic File Folder", "brand": "Gitanjali", "copy": "Lightweight document storage for school, office and personal use.", "image": "plastic.jpg"},
    {"category_slug": "papers", "name": "A4 Copier Paper",     "brand": "Paper",     "copy": "Reliable everyday paper for printing, copying, documentation and office work.", "image": "paper.jpg"},
    {"category_slug": "papers", "name": "Colour Paper",        "brand": "Paper",     "copy": "Colourful paper for school projects, office presentations and creative work.", "image": "colorpaper.jpg"},

    # Supplies
    {"category_slug": "supplies", "name": "Stapler",           "brand": "Kangaro",  "copy": "Strong and dependable staplers for everyday office paperwork.", "image": "stepler.jpg"},
    {"category_slug": "supplies", "name": "Paper Punch",       "brand": "Kangaro",  "copy": "Precision paper punches for organised filing and document preparation.", "image": "punch.jpg"},
    {"category_slug": "supplies", "name": "Adhesive Tape",     "brand": "Pidilite", "copy": "Useful adhesive solutions for packaging, office work and everyday tasks.", "image": "tap.jpg"},
    {"category_slug": "supplies", "name": "Gel Pens",          "brand": "Cello",    "copy": "Smooth-flowing pens designed for comfortable everyday writing.", "image": "gelpen.jpg"},
    {"category_slug": "supplies", "name": "Permanent Marker",  "brand": "Artline",  "copy": "Bold permanent markers for labels, packaging, boards and general use.", "image": "marker.jpg"},
    {"category_slug": "supplies", "name": "Whiteboard Marker", "brand": "Artline",  "copy": "Clear, easy-to-read markers for classrooms, offices and presentations.", "image": "whitemarker.jpg"},

    # Art & Craft
    {"category_slug": "art-craft", "name": "Art Colour Set",  "brand": "DOMS",     "copy": "Creative colour supplies for students, artists and craft projects.", "image": "artcolorset.jpg"},
    {"category_slug": "art-craft", "name": "Craft Adhesive",  "brand": "Pidilite", "copy": "Trusted adhesive for school projects, crafts and everyday creative work.", "image": "craft.jpg"},
]


class Command(BaseCommand):
    help = "Import the built-in CATEGORIES and PRODUCTS into the database."

    def handle(self, *args, **options):
        # 1. Categories
        cat_map = {}
        for i, c in enumerate(CATEGORIES):
            cat, created = Category.objects.update_or_create(
                slug=c["slug"],
                defaults={
                    "name": c["name"],
                    "icon": c.get("icon", ""),
                    "blurb": c.get("blurb", ""),
                    "order": i,
                },
            )
            cat_map[c["slug"]] = cat
            self.stdout.write(f"{'Created' if created else 'Updated'} category: {cat.name}")

        # 2. Products
        for i, p in enumerate(PRODUCTS):
            cat = cat_map.get(p["category_slug"])
            if not cat:
                self.stderr.write(f"No category for {p['name']}")
                continue

            prod, created = Product.objects.update_or_create(
                name=p["name"],
                category=cat,
                defaults={
                    "brand": p.get("brand", ""),
                    "copy": p.get("copy", ""),
                    "order": i,
                },
            )

            # Try to attach the image from static folder if it exists and hasn't been attached yet
            if not prod.image:
                static_path = (
                    Path(settings.BASE_DIR)
                    / "store" / "static" / "store" / "images" / p["image"]
                )
                if static_path.exists():
                    with static_path.open("rb") as f:
                        prod.image.save(static_path.name, File(f), save=True)
                    self.stdout.write(f"  ↳ Attached image {static_path.name}")
                else:
                    self.stdout.write(f"  ↳ (no file found at {static_path})")

            self.stdout.write(f"{'Created' if created else 'Updated'} product: {prod}")

        self.stdout.write(self.style.SUCCESS("✔ Seeding complete."))