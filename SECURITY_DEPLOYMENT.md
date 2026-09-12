# Gitanjali Security / Deployment Notes

## Production environment variables

Set these on the production server:

DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<long-random-secret-key>

Do not commit the production secret key to Git or publish it in the ZIP.

## Local development

For local development:

DJANGO_DEBUG=True
DJANGO_SECRET_KEY=<optional-development-secret>

The settings file allows localhost and 127.0.0.1 only when DEBUG=True.

## Production admin URL

The Django admin is available at:

/gitanjali-management/

The default /admin/ URL is intentionally not registered.

This URL change is only an additional layer. Django authentication and staff permissions still protect the admin.

## Required checks

Run:

python manage.py check
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic --noinput

## HTTPS

Production settings redirect HTTP to HTTPS and enable secure cookies and HSTS.

Before enabling HSTS preload, make sure the domain and every HTTPS subdomain are permanently configured for HTTPS.

## Important

The SQLite database is suitable for a small/simple site, but for a growing production application consider PostgreSQL.
