# Gitanjali Stationery Store — Django

A Django version of the blue-and-white Gitanjali storefront for stationery, printing, and custom rubber stamps.

## Run locally (without a virtual environment)

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

On Windows, use `py` instead of `python` if that is how Python is installed.

Open `http://127.0.0.1:8000/`.

## Included pages

- `/` — home
- `/stationery/` — stationery catalog with category filtering and request-list interactions
- `/printing/` — printing services and brief form
- `/rubber-stamps/` — rubber stamp services and quote form
- `/about/` — store story and capabilities
- `/contact/` — contact information and server-validated quote request
- Customer reviews — visitors can submit a rating and review from the homepage; reviews are persisted in SQLite and can be managed from Django admin

## Project structure

- `gitanjali_site/` — Django project settings and URL configuration
- `store/` — app views, forms, routes, and templates
- `static/store/` — CSS and JavaScript for the storefront

The quote form validates on the server and opens a pre-filled WhatsApp message. Customer reviews are stored locally in the configured database. Product images are bundled locally so the stationery catalogue does not depend on external image hosts.