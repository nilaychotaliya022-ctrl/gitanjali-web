from django.db import models


# =========================================================
# CATEGORY
# =========================================================

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    icon = models.CharField(
        max_length=8, blank=True,
        help_text="Emoji or symbol, e.g. ✎"
    )
    blurb = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT
# =========================================================

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=120)
    brand = models.CharField(max_length=80, blank=True)
    copy = models.TextField(help_text="Short description shown on the tile.")
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__order", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.brand})" if self.brand else self.name


# =========================================================
# REVIEW
# Fields match your existing ReviewForm:
#   name, context, rating, quote
# =========================================================

class Review(models.Model):
    name = models.CharField(max_length=120)
    context = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.rating}★"