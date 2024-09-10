from ..models import Contact


def save_contact(contact: Contact, related_products) -> Contact:
    contact.save()
    contact.products.set(related_products)
    return contact
