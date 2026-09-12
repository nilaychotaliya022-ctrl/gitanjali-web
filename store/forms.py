from django import forms

from .models import Review


class QuoteForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        label="Your name",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Meera Shah"}),
    )
    phone = forms.CharField(
        max_length=30,
        label="Phone number",
        widget=forms.TextInput(attrs={"placeholder": "e.g. 98765 43210"}),
    )
    service = forms.ChoiceField(
        required=False,
        label="I need help with",
        choices=[
            ("", "Select a service"),
            ("stationery", "Stationery list"),
            ("printing", "Printing"),
            ("stamp", "Custom rubber stamp"),
            ("other", "Not sure yet"),
        ],
    )
    deadline = forms.CharField(
        max_length=120,
        required=False,
        label="Needed by",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Friday afternoon"}),
    )
    details = forms.CharField(
        max_length=300,
        label="Short message",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Example: 20 office stamps needed by Friday.",
                "rows": 2,
                "maxlength": "300",
            }
        ),
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("name", "context", "rating", "quote")
        labels = {
            "name": "Your name",
            "context": "What do you do?",
            "rating": "Your rating",
            "quote": "Your review",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Meera Shah"}),
            "context": forms.TextInput(attrs={"placeholder": "e.g. Office administrator"}),
            "rating": forms.Select(choices=[(value, f"{value} star{'s' if value != 1 else ''}") for value in range(1, 6)]),
            "quote": forms.Textarea(attrs={"placeholder": "What did we help you get done?", "rows": 4}),
        }