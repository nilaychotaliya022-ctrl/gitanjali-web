from django.urls import path

from . import views


urlpatterns = [
    path("",                views.home,          name="home"),
    path("stationery/",     views.stationery,    name="stationery"),
    path("products/",       views.all_products,  name="all_products"),
    path("printing/",       views.printing,      name="printing"),
    path("rubber-stamps/",  views.rubber_stamps, name="rubber_stamps"),
    path("about/",          views.about,         name="about"),
    path("contact/",        views.contact,       name="contact"),
]