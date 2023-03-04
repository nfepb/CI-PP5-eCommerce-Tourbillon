from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Creates the Product form information
    """
    class Meta:
        model = Product
        # Include all the fields
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
            "watch_details": SummernoteWidget(),
            "features": SummernoteWidget(),
        }

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        # Override init method to make a few changes to fields
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        # List comprehension associating friendly name to category ID.
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields["category"].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "border-secondary rounded-1"


class CategoryForm(forms.ModelForm):
    """ Category form"""
    class Meta:
        """category model fields"""
        model = Category
        fields = '__all__'
