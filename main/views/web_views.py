from django.shortcuts import render, redirect
from main.models import Faq, FaqCategory, Classification
from main.forms import CheckoutForm, ContactForm
from ..services.cart_service import get_cart
from ..services.order_service import save_checkout_form
from ..services.price_service import get_all_price_data
from ..services.contact_service import save_contact
from .request_utils import get_session_id


def index_view(response):
    return render(response, "main/home.html", {})


def menu_view(request):
    classifications = Classification.objects.prefetch_related('product_set__stock').all().order_by("order")

    # go back to the products page
    return render(request, 'main/menu.html', {
        'classifications': classifications,  # includes products (and product stock where applicable)
        'cartItems': get_cart(get_session_id(request)).cart_items.all()
    })


def checkout_view(request):
    if request.method == "POST":

        if request.POST.get("form_type") == "checkout":
            form = CheckoutForm(request.POST)

            if form.is_valid():
                order = save_checkout_form(form, get_cart(get_session_id(request)))
                item_list = order.order_products.all()

                return render(request, "main/order-confirmed.html", {
                    "item_list": item_list,
                    "order_id": order.id,
                    "order_date": order.created_date,
                    "update_allowed": False,
                    "price_data": get_all_price_data(item_list)
                })
            else:
                session_id = get_session_id(request)
                cart = get_cart(session_id)
                item_list = cart.cart_items.all()

                # if the form contains errors this will be returned in the context below and displayed on screen
                return render(request, "main/checkout.html",
                          {
                              "form": form,
                              "item_list": item_list,
                              "update_allowed": True,
                              "price_data": get_all_price_data(item_list)})

    else:
        form = CheckoutForm()
        session_id = get_session_id(request)
        cart = get_cart(session_id)
        item_list = cart.cart_items.all()

        return render(request, "main/checkout.html",
                      {
                          "form": form,
                          "item_list": item_list,
                          "update_allowed": True,
                          "price_data": get_all_price_data(item_list)})


def about_view(request):
    return render(request, "main/about.html", {})


def order_view(request):
    session_id = get_session_id(request)
    item_list = get_cart(session_id).cart_items.all()
    return render(request, "main/order.html",
                  {"price_data": get_all_price_data(item_list),
                   "update_allowed": True,
                   "item_list": item_list})


def faq_view(request):
    faq_list = Faq.objects.filter(active=True)
    faq_category_list = FaqCategory.objects.filter(active=True).order_by("order")
    return render(request, "main/faq.html", {"faqs": faq_list, "category_list": faq_category_list})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = save_contact(form)
            return redirect("contact_submitted", contact_type=contact.type.type)

        else:
            # if the form contains errors this will be returned in the context below and displayed on screen
            return render(request, "main/contact.html", {"form": form})

    else:
        # create a new form and pass it into the page
        form = ContactForm
        return render(request, "main/contact.html", {"form": form})


def contact_submitted_view(request, contact_type):
    return render(request, 'main/contact-submitted.html', {'contact_type': contact_type})

