from django.db import models
from django.shortcuts import reverse
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    info = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('contacts_page_url')
