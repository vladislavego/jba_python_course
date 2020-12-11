from django.urls import path
from .views import *

urlpatterns = [
    path('', ContactsPage.as_view(), name='contacts_page_url'),
]