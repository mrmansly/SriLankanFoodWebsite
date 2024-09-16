from django import template

register = template.Library()


@register.filter
def multiply(value,arg):
    try:
        result = float(value) * float(arg)
        return f"{result:.2f}"
    except (ValueError, TypeError):
        return 'Undefined'


@register.filter
def chilli_range(value):
    return range(0, value)


@register.filter
def filter_by_category(queryset, category):
    return queryset.filter(category=category)


@register.filter
def use_cart_item_quantity(product_id, args):
    cart = args
    cart_items = cart.cartitem_set.filter(product_id=product_id)
    quantity = 0

    for cart_item in cart_items:
        quantity += cart_item.quantity

    return quantity
