from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseServerError
from .models import Cart, Contact, Order, Faq, FaqCategory, OrderProduct, Product, Classification
from .forms import CheckoutForm, ContactForm
from datetime import datetime
import json
from .services.cart_service import get_cart, add_product, update_quantity, get_cart_items
from .services.order_service import create_order
from .services.price_service import get_total_price, get_all_price_data
from .services.contact_service import save_contact
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CartSerializer, CartItemSerializer, ContactSerializer
from .exceptions import ValidationException


# Create your views here.


def index_view(response):
    return render(response, "main/home.html", {})


# def add_item_to_cart(session_id, product_id, quantity):
#     cart: Cart = get_cart(session_id)
#     add_product(cart.id, product_id, quantity)


def products_view(response):
    return render_product_page(response)


def checkout_view(response):
    if response.method == "POST":

        if response.POST.get("form_type") == "checkout":
            form = CheckoutForm(response.POST)

            if form.is_valid():
                order = Order()
                order.first_name = form.cleaned_data["first_name"]
                order.last_name = form.cleaned_data["last_name"]
                order.email = form.cleaned_data["email"]
                order.mobile = form.cleaned_data["mobile"]
                order.home_phone = form.cleaned_data["home_phone"]
                order.created_date = datetime.now()

                cart = get_cart(get_session_id(response))
                order.total_price = get_total_price(cart.cartitem_set.all())

                order = create_order(order, cart)
                item_list = order.orderproduct_set.all()

                return render(response, "main/order-confirmed.html", {
                    "item_list": item_list,
                    "order_id": order.id,
                    "order_date": order.created_date,
                    "update_allowed": False,
                    "price_data": get_all_price_data(item_list)
                })
            else:
                print("Form is invalid")

        elif response.POST.get("form_type") == "quantity":
            product_id = int(response.POST.get("product_id"))
            quantity = int(response.POST.get("quantity"))

            session_id = get_session_id(response)
            cart = get_cart(session_id)

            update_quantity(cart.id, product_id, quantity)
            form = CheckoutForm()
            item_list = cart.cartitem_set.all()  # if cart.cartitem_set.exists() else None

            return render(response, "main/checkout.html", {"form": form,
                                                           "item_list": item_list,
                                                           "update_allowed": True,
                                                           "price_data": get_all_price_data(item_list)})

    else:
        form = CheckoutForm()
        session_id = get_session_id(response)
        cart = get_cart(session_id)
        item_list = cart.cartitem_set.all()  # if cart.cartitem_set.exists() else None

        return render(response, "main/checkout.html", {"form": form,
                                                       "item_list": item_list,
                                                       "update_allowed": True,
                                                       "price_data": get_all_price_data(item_list)})


def cart_view(response, cart_id):
    cart_obj = Cart.objects.get(id=cart_id)
    cart_item = cart_obj.cartitem_set.get(id=cart_id)

    price = f"{cart_item.product.price:.2f}"
    # return HttpResponse("<h1>%s</h1>" % cartItem.product.name % cartItem.product.price)
    return HttpResponse("<h1>%s $ %s</h1>" % (cart_item.product.name, str(price)))


# def order_confirmed_view(response):
#     order_id = response.session.get('order_id')
#     order = Order.objects.get("id", order_id)
#     item_list = order.orderproduct_set.all()
#     return render(response, "main/order-confirmed.html", {
#         "item_list": item_list,
#         "price_data": get_all_price_data(item_list)
#     })


def about_view(response):
    return render(response, "main/about.html", {})


def order_view(response):
    session_id = get_session_id(response)

    if response.method == "POST" and response.POST.get("form_type") == "quantity":
        product_id = int(response.POST.get("product_id"))
        quantity = int(response.POST.get("quantity"))

        cart = get_cart(session_id)

        if cart is not None:
            update_quantity(cart.id, product_id, quantity)

    item_list = get_cart(session_id).cartitem_set.all()
    return render(response, "main/order.html",
                  {"price_data": get_all_price_data(item_list),
                   "update_allowed": True,
                   "item_list": item_list})


def faq_view(response):
    faq_list = Faq.objects.filter(active=True)
    faq_category_list = FaqCategory.objects.filter(active=True).order_by("order")
    return render(response, "main/faq.html", {"faqs": faq_list, "category_list": faq_category_list})


def create_contact_from_form(form):
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

def contact_view(response):
    if response.method == "POST":
        form = ContactForm(response.POST)

        # print(form.product)
        # print(form.product.widget)

        if form.is_valid():
            # try:
                contact, related_products = create_contact_from_form(form)
                contact = save_contact(contact, related_products)
                return redirect("contact_submitted", contact_type=contact.type.type)

            # except ValidationException as e:
            #     return render(response, "main/contact.html", {"form": form, "validation_error": e.message})
            # except Exception as e:
            #     # Unexpected Error
            #     return HttpResponseServerError("Base Exception Error:" + str(e))

        else:
            # if the form contains errors this will be returned in the context below and displayed on screen
            return render(response, "main/contact.html", {"form": form})

    else:
        # create a new form and pass it into the page
        form = ContactForm
        return render(response, "main/contact.html", {"form": form})


def render_product_page(request):
    classifications = Classification.objects.all().order_by("order")
    product_list = Product.objects.all()

    # display a success message that contact was submitted, but for now just
    # go back to the products page
    return render(request, 'main/products.html', {
        'products': product_list,
        'classifications': classifications
    })


def get_session_id(response):
    session_id = response.session.session_key

    if session_id is None:
        response.session.create()
        session_id = response.session.session_key

    return session_id


def contact_submitted_view(request, contact_type):
    return render(request, 'main/contact-submitted.html', {'contact_type': contact_type})


@api_view(['POST'])
# May need to consider CORS for handling this in other environments??
def api_gateway_view(request, api_path):
    print(api_path)
    if api_path == 'update-cart-item-quantity':
        request_body = request.data
        add_product(int(request_body['cart_id']),
                    int(request_body['product_id']),
                    int(request_body['quantity']))

        cart_items = get_cart_items(int(request_body['cart_id']))
        cart_item_serializer = CartItemSerializer(cart_items, many=True)
        return Response(cart_item_serializer.data)
    else:
        data = {
            'message': 'Hello from Django!'
        }
    return JsonResponse(data)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
