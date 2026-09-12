from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("customer", "context", "rating_display", "quote_preview", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("name", "context", "quote")
    ordering = ("-created_at",)
    list_per_page = 12
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)

    @admin.display(description="Customer", ordering="name")
    def customer(self, obj):
        return obj.name

    @admin.display(description="Rating", ordering="rating")
    def rating_display(self, obj):
        return "★" * obj.rating + "☆" * (5 - obj.rating)

    @admin.display(description="Review")
    def quote_preview(self, obj):
        text = obj.quote.strip()
        return text if len(text) <= 80 else text[:80] + "…"
