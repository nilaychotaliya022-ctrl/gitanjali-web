# Gitanjali Stationery & Rubber Stamp — Django Website

Premium blue-and-white Django storefront for Gitanjali Stationery & Rubber Stamp, including stationery, printing and custom rubber stamps.

## Important: Python version

This project uses Django 5.x. **Use 64-bit Python 3.11 or newer (up to the supported Django version)**.

If your Windows PC is using the old **Python 3.8 32-bit**, do not run this project with that interpreter. Django 5.x does not support Python 3.8, and the old interpreter can cause installation/runtime failures.

Check your version:

```powershell
py --version
python --version
```

## Run locally on Windows — no virtual environment required

From the project folder:

```powershell
py -3.11 -m pip install -r requirements.txt
```

Create a local `.env` from `.env.example`, or set development variables in PowerShell:

```powershell
$env:DJANGO_DEBUG="True"
$env:DJANGO_SECRET_KEY="local-development-key-change-this"
$env:DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
$env:DJANGO_CSRF_TRUSTED_ORIGINS="http://127.0.0.1:8000,http://localhost:8000"
```

Then:

```powershell
py -3.11 manage.py migrate
py -3.11 manage.py check
py -3.11 manage.py runserver
```

Open:

`http://127.0.0.1:8000/`

## Production / PythonAnywhere

Set these environment variables in the hosting environment:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY=<long-random-secret>`
- `DJANGO_ALLOWED_HOSTS=gitanjalistationary.com,www.gitanjalistationary.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://gitanjalistationary.com,https://www.gitanjalistationary.com`

Do **not** commit `.env` or production secrets to GitHub.

## Main pages

- `/` — Home
- `/stationery/` — stationery catalogue
- `/products/` — all products
- `/printing/` — printing services
- `/rubber-stamps/` — custom rubber stamps
- `/about/` — store story and reviews
- `/contact/` — WhatsApp quote/contact form
- `/gitanjali-management/` — Django admin

## Responsive improvements included

- Mobile-first header and hamburger navigation
- Touch-friendly buttons and form controls
- Mobile Call / WhatsApp / Get Quote action bar
- Responsive product, service, machine and stamp grids
- Horizontal mobile filter controls instead of overflowing the page
- Safer wrapping for long addresses, emails and product names
- Responsive stationery, printing, rubber-stamp, about and contact layouts
- Reduced-motion support
- Fixed missing logo/static references
- Removed a missing rubber-stamp video poster reference
- Fixed development static-file routing so Django's staticfiles app can serve CSS/JS correctly

## Dependencies

`requirements.txt` includes Django plus the packages used by the current settings:

- Django
- django-axes
- django-csp
- python-dotenv
- Pillow
