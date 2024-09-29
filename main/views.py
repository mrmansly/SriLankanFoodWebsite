from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main.models import Cart, Contact, Faq, FaqCategory, Product, Classification, ContactType
from main.forms import CheckoutForm, ContactForm
from .services.cart_service import get_cart, add_product, update_cart_details
from .services.order_service import save_checkout_form
from .services.price_service import get_all_price_data
from .services.contact_service import save_contact
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CartSerializer, ContactSerializer, ProductSerializer, ClassificationSerializer, \
    ContactTypeSerializer, FaqCategorySerializer, FaqSerializer
from django.core.exceptions import ValidationError


def index_view(response):
    return render(response, "main/home.html", {})


def menu_view(request):
    classifications = Classification.objects.all().order_by("order")
    product_list = Product.objects.all()

    # display a success message that contact was submitted, but for now just
    # go back to the products page
    return render(request, 'main/menu.html', {
        'products': product_list,
        'classifications': classifications,
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
                raise ValidationError("Form is invalid!")

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


def get_session_id(request):
    session_id = request.session.session_key

    if session_id is None:
        request.session.create()
        session_id = request.session.session_key

    return session_id


def contact_submitted_view(request, contact_type):
    return render(request, 'main/contact-submitted.html', {'contact_type': contact_type})


def get_serialized_cart(request):
    cart = get_cart(get_session_id(request))
    cart_serializer = CartSerializer(cart, many=False)
    return cart_serializer.data


@api_view(['POST'])
def api_gateway_view(request, api_path):
    if api_path == 'update-cart-item-quantity':
        request_body = request.data
        add_product(int(request_body['cart_id']),
                    int(request_body['product_id']),
                    int(request_body['quantity']),
                    request_body['instructions'])

        return Response(get_serialized_cart(request))
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer


class ContactTypeViewSet(viewsets.ModelViewSet):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class FaqCategoryViewSet(viewsets.ModelViewSet):
    queryset = FaqCategory.objects.all()
    serializer_class = FaqCategorySerializer


class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
