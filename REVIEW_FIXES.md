# Gitanjali Website Review & Fixes

## Bugs found and fixed

1. **Stationery page CSS file was missing**
   - `stationery.html` loaded `store/css/stationery.css`, but the file was absent.
   - Added a complete responsive `stationery.css`.

2. **Stationery page JavaScript file was missing**
   - `stationery.html` loaded `store/js/stationery.js`, but the file was absent.
   - Added `stationery.js`.

3. **Product filters had two competing JavaScript implementations**
   - `site.js` contained an older filter implementation and a newer implementation.
   - The old code used the `hidden` HTML attribute and checked for `All`, while the page uses lowercase `all`.
   - This could make the "All" filter hide products even after the newer code tried to show them.
   - Replaced `site.js` with one unified implementation.

4. **Footer CSS was being overridden by legacy footer rules**
   - `site.css` contained older `.footer` / `.footer-grid` rules after the newer footer styles.
   - Added a final footer override so the premium footer consistently wins.

5. **Contact page address was not clickable**
   - Changed the store address to a Google Maps link.

6. **Opening-hours text was inconsistent**
   - Base footer/top bar and contact page used different hours.
   - Contact page now uses Mon–Sat, 8:30 am–8:30 pm to match the site-wide text.

7. **Static deployment setting**
   - Added `STATIC_ROOT = BASE_DIR / "staticfiles"` for `collectstatic`.

8. **Domain host configuration**
   - Added `gitanjalistationary.com` and `www.gitanjalistationary.com` to `ALLOWED_HOSTS`.

## Important deployment note

Before production deployment, set `DEBUG = False`, use a real secret key, configure HTTPS/security settings, and run:

```bash
python3 manage.py collectstatic --noinput
python3 manage.py migrate
python3 manage.py check
```

The local environment used for this review did not have Django installed, so Django's runtime `manage.py check` could not be executed here. JavaScript syntax was checked successfully with Node.js.
