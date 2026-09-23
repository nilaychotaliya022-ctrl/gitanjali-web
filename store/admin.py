from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, Review


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "order", "product_count")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    ordering = ("order", "name")

    @admin.display(description="Products")
    def product_count(self, obj):
        return obj.products.count()


# =========================================================
# PRODUCT — with image upload + preview
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "brand", "category", "is_active", "order")
    list_display_links = ("thumb", "name")
    list_editable = ("is_active", "order")
    list_filter = ("category", "is_active", "brand")
    search_fields = ("name", "brand", "copy")
    autocomplete_fields = ("category",)
    save_on_top = True

    fieldsets = (
        ("Product info", {
            "fields": ("name", "brand", "category", "copy")
        }),
        ("Image", {
            "fields": ("image", "preview"),
            "description": "Upload a product image (JPG/PNG/WebP). "
                           "It will be saved under /media/products/."
        }),
        ("Visibility", {
            "fields": ("is_active", "order")
        }),
    )
    readonly_fields = ("preview",)

    @admin.display(description="Image")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:42px;width:42px;'
                'object-fit:cover;border-radius:6px;'
                'border:1px solid #e5e0d5;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:240px;'
                'border-radius:12px;border:1px solid #e5e0d5;" />',
                obj.image.url,
            )
        return "No image uploaded yet."


# =========================================================
# REVIEW
# =========================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "context", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("name", "context", "quote")
    ordering = ("-created_at",)