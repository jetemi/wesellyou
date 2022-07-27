"""Forms for 'products' app - shop"""
from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    '''Product form for admin user to add/edit product from frontend'''
    class Meta:
        '''
        Form based on Product model.
        Helptexts and labels specified for some fields.
        Image field - use custom file input widget that overrides Django one
        '''
        model = Product
        fields = '__all__'
        labels = {
            'is_active': 'Active product?',
            'is_new': 'New product?',
        }
        help_texts = {
            'name': 'Product name must be unique',
            'category': 'If category is not in list, you can add a new one',
            'is_active': 'Only active products are visible in the shop to '
            'users. Leave un-checked if product not ready to be shown in shop',
            'is_new': 'A "New!" badge will be shown on the product if this '
            'is ticked',
        }

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
        )

    def __init__(self, *args, **kwargs):
        """
        Override init method to make changes to fields:
        Create tuple of category ids and friendly names, use this to set the
        choices in the category field dropdown. Add css class to all fields.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names
        self.fields['category'].choices.insert(
            0, ('', 'Choose category from the list')
            )
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'brand-form-input'
