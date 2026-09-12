from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    name = models.CharField(max_length=80)
    context = models.CharField(max_length=80)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    quote = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} ({self.rating}/5)"