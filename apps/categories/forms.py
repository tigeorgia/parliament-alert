from django import forms
from parliament.apps.categories.models import Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label="Category name",
        max_length=50,
        help_text="This category's name.")

    keywords = forms.CharField(
        label="Keywords",
        max_length=300,
        help_text="Comma-delimited set of keywords that will match this category.",
        widget=forms.widgets.Textarea({
            "cols": 30,
            "rows": 4}))

    class Meta:
        model = Category
