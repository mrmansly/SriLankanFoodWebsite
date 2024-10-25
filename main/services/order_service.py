from django.template.loader import render_to_string
from ..models import Order, OrderProduct, ProductStock
from .email_service import send_email
from .price_service import get_all_price_data, get_total_price
from django.utils import timezone
from ..enums import EmailConfigurationType
from django.core.exceptions import ObjectDoesNotExist


def save_checkout_form(form, cart) -> Order:
    order = Order()
    order.first_name = form.cleaned_data["first_name"]
    order.last_name = form.cleaned_data["last_name"]
    order.email = form.cleaned_data["email"]
    order.mobile = form.cleaned_data["mobile"]
    order.home_phone = form.cleaned_data["home_phone"]
    order.requested_delivery_date = form.cleaned_data["requested_delivery_date"]
    order.created_date = timezone.now()

    order.total_price = get_total_price(cart.cart_items.all())

    return create_order(order, cart)


def create_order(order, cart) -> Order:
    order.save()

    save_order_products(order, cart.cart_items.all())

    # remove the cart after it has been converted to an order as no longer needed
    cart.delete()

    # notify the submitter via email.
    try:
        send_email(EmailConfigurationType.ORDER_CONFIRMATION, order.email,
                   "Order Confirmation " + str(order.id),
                   create_confirmation_body_html(order),
                   create_confirmation_body_plain(order))
        order.confirmation_sent_date = timezone.now()
        order.save()
    except Exception as e:
        # if email fails to send, there will be another job to check for this and resend so that the order doesn't
        # get ignored.
        print(f"Error sending email: {e}")

    return order


def save_order_products(order, cart_items):
    for cart_item in cart_items:
        order_item = OrderProduct(product=cart_item.product,
                                  order=order,
                                  quantity=cart_item.quantity,
                                  instructions=cart_item.instructions)
        order_item.save()
        decrement_product_stock(order_item)


def decrement_product_stock(order_item):
    try:
        product_stock = ProductStock.objects.get(product=order_item.product)
        product_stock.quantity = product_stock.quantity - order_item.quantity

        if product_stock.quantity < 0:
            product_stock.quantity = 0

        product_stock.save()

    except ObjectDoesNotExist:
        # if no product stock is found for this product then no reduction in quantity is needed
        pass


def create_confirmation_body_html(order: Order):
    subject = 'Order Confirmation ' + str(order.id)
    item_list = order.order_products.all()
    html_content = render_to_string(
        'main/email-order-confirmation-template.html',
        {
            "subject": subject,
            "item_list": item_list,
            "order": order,
            "price_data": get_all_price_data(item_list)}
    )

    return html_content


def create_confirmation_body_plain(order: Order):
    subject = 'Order Confirmation ' + str(order.id)
    item_list = order.order_products.all()

    txt_content = render_to_string(
        'main/email-order-confirmation-template.txt',
        {
            "subject": subject,
            "order": order,
            "item_list": item_list,
            "price_data": get_all_price_data(item_list)
        }
    )

    return txt_content
