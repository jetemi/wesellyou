'''Forms fr profiles app - UserProfileForm'''
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    """form for default delivery details on user profile"""
    class Meta:
        """
        Form based on UserProfile model, but exclude user as this
        will not change (it's linked to User model).
        """
        model = UserProfile
        exclude = ('user',)
        labels = {
            'default_street_address1': 'Default Street address 1',
            'default_street_address2': 'Default Street address 2',
        }

    def __init__(self, *args, **kwargs):
        """
        Override init method to add placeholders for some fields
        add class for CSS, set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_postcode': 'Postal Code',
        }
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders.keys():
                self.fields[field].widget.attrs['placeholder'] = (
                    placeholders[field]
                    )
            if field == 'default_country':
                self.fields[field].widget.attrs['class'] = (
                    'brand-form-input country-input'
                    )
            else:
                self.fields[field].widget.attrs['class'] = 'brand-form-input'
