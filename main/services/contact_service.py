from ..models import Contact, Product
from datetime import datetime


def save_contact(form) -> Contact:

    contact, related_products = create_from_form(form)
    contact.save()
    contact.products.set(related_products)
    return contact


def create_from_form(form):
    contact = Contact()
    contact.type = form.cleaned_data["type"]
    contact.title = form.cleaned_data["title"]
    contact.message = form.cleaned_data["message"]
    contact.preferred_contact = form.cleaned_data["preferred_contact"]
    contact.response_required = form.cleaned_data['response_required']
    contact.email = form.cleaned_data['email']
    contact.mobile = form.cleaned_data['mobile']
    contact.home_phone = form.cleaned_data['home_phone']
    contact.rating = form.cleaned_data['rating']
    contact.created_date = datetime.now()

    related_products = form.cleaned_data['products']
    return contact, related_products
