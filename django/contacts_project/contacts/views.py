from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import View

from .forms import *
from .models import *

class ContactsPage(View):
    def get(self, request):
        if request.is_ajax():
            if request.GET.get('action') == 'show':
                contacts = Contact.objects.all()       
                contacts_table = render_to_string('contacts/includes/contacts_table.html', {'contacts': contacts})
                return JsonResponse({'contacts_table': contacts_table})
            elif request.GET.get('action') == 'hide':
                contacts_table = render_to_string('contacts/includes/contacts_table.html')
                return JsonResponse({'contacts_table': contacts_table})

           
        contact_form = ContactForm()
        return render(request, 'contacts/contacts.html', context={'contact_form': contact_form})

    def post(self, request):
        data = request.POST
        new_contact = ContactForm(data)
        if new_contact.is_valid():
            contact = new_contact.save()
            contact_description = render_to_string('contacts/includes/new_contact.html', {'contact': contact})
            new_contact_form = ContactForm()
            contact_form = render_to_string('contacts/includes/contact_form.html', {'contact_form': new_contact_form}, request)
            return JsonResponse({'contact_form': contact_form, 'contact_description': contact_description})
            
        contact_form = render_to_string('contacts/includes/contact_form.html', {'contact_form': new_contact}, request)
        return JsonResponse({'contact_form': contact_form})

    



