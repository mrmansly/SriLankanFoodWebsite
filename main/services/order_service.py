from django.template.loader import render_to_string
from ..models import Order, OrderProduct
from . email_service import send_email
from . price_service import get_total_price, get_gst, get_net_cost, get_all_price_data


def create_order(order, cart):

    order.save()

    for cart_item in cart.cartitem_set.all():
        order_item = OrderProduct(product=cart_item.product,
                                  order=order,
                                  quantity=cart_item.quantity,
                                  instructions=cart_item.instructions)
        order_item.save()

    # remove the cart after it has been converted to an order
    cart.delete()

    # notify the submitter via email
    send_email(order.email, "Order Confirmation " + str(order.id),
                            create_confirmation_body_html(order), create_confirmation_body_plain(order))

    return order


def create_confirmation_body_html(order: Order):

    subject = 'Order Confirmation ' + str(order.id)
    item_list = order.orderproduct_set.all()
    html_content = render_to_string(
        'main/email-order-confirmation-template.html',
        {
            "subject": subject,
            "item_list": item_list,
            "order": order,
            "price_data": get_all_price_data(item_list)}
    )

    print(html_content)
    return html_content


def create_confirmation_body_plain(order: Order):

    subject = 'Order Confirmation ' + str(order.id)
    item_list = order.orderproduct_set.all()

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
