from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'info']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Contact.objects.filter(phone_number=phone_number).count():
            raise ValidationError('Number already exist.')
        return phone_number

