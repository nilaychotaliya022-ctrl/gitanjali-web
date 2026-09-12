from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


# ============================================================
# ROBOTS.TXT
# ============================================================

def robots(request):
    return HttpResponse(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /gitanjali-management/\n\n"
        "Sitemap: "
        + request.build_absolute_uri("/sitemap.xml")
        + "\n",
        content_type="text/plain",
    )


# ============================================================
# SITEMAP.XML
# ============================================================

def sitemap(request):
    urls = [
        "/",
        "/stationery/",
        "/printing/",
        "/rubber-stamps/",
        "/about/",
        "/contact/",
    ]

    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    )

    for url in urls:
        body += (
            "<url>"
            "<loc>"
            + request.build_absolute_uri(url)
            + "</loc>"
            "</url>"
        )

    body += "</urlset>"

    return HttpResponse(body, content_type="application/xml")


# ============================================================
# MAIN URL CONFIGURATION
# ============================================================

# Custom branded error handlers. Django uses these when DEBUG=False.
from django.views.defaults import bad_request, permission_denied, page_not_found, server_error

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error


urlpatterns = [
    # SEO endpoints
    path("robots.txt", robots, name="robots"),
    path("sitemap.xml", sitemap, name="sitemap"),

    # Protected Django administration.
    # Django Admin still requires authentication and staff permissions.
    path("gitanjali-management/", admin.site.urls),

    # Public website
    path("", include("store.urls")),
]
