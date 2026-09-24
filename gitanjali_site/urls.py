from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import (
    bad_request,
    permission_denied,
    page_not_found,
    server_error,
)


# ============================================================
# ROBOTS.TXT
# ============================================================

def robots(request):
    """
    Serve a robots.txt that allows the public site but blocks
    the Django admin from being indexed by search engines.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /gitanjali-management/",
        "Disallow: /admin/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ============================================================
# SITEMAP.XML
# ============================================================

def sitemap(request):
    """
    Minimal hand-rolled sitemap. For larger sites, use
    django.contrib.sitemaps instead.
    """
    from xml.sax.saxutils import escape

    urls = [
        {"loc": "/",              "changefreq": "weekly",  "priority": "1.0"},
        {"loc": "/stationery/",   "changefreq": "monthly", "priority": "0.8"},
        {"loc": "/printing/",     "changefreq": "monthly", "priority": "0.8"},
        {"loc": "/rubber-stamps/","changefreq": "monthly", "priority": "0.8"},
        {"loc": "/about/",        "changefreq": "yearly",  "priority": "0.5"},
        {"loc": "/contact/",      "changefreq": "yearly",  "priority": "0.5"},
    ]

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for item in urls:
        loc = escape(request.build_absolute_uri(item["loc"]))
        parts.append(
            "<url>"
            f"<loc>{loc}</loc>"
            f"<changefreq>{item['changefreq']}</changefreq>"
            f"<priority>{item['priority']}</priority>"
            "</url>"
        )

    parts.append("</urlset>")
    return HttpResponse("".join(parts), content_type="application/xml")


# ============================================================
# ERROR HANDLERS
# ============================================================

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [
    # SEO endpoints
    path("robots.txt", robots, name="robots"),
    path("sitemap.xml", sitemap, name="sitemap"),

    # Protected Django administration.
    path("gitanjali-management/", admin.site.urls),

    # Public website (must be last — catch-all)
    path("", include("store.urls")),
]


# ============================================================
# DEV-ONLY: serve media & static files
# ============================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ============================================================
# ADMIN BRANDING
# ============================================================
admin.site.site_header = "Gitanjali Control Desk"
admin.site.site_title = "Gitanjali Admin"
admin.site.index_title = "Stationery & Rubber Stamp Management"