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
    if category is not None:
        return queryset.filter(category=category)

    return None


@register.filter
def use_cart_item_quantity(product_id, args):
    cart = args
    cart_items = cart.cart_items.filter(product_id=product_id)
    quantity = 0

    # should only ever expect 0 or 1 items to be returned in above filter call, but handle multiple
    # cart_items with the same product in any case (ie. Maybe to allow different quantities of the same
    # product to have different special instructions in the future).
    for cart_item in cart_items:
        quantity += cart_item.quantity

    return quantity


@register.filter
def use_cart_item_instructions(product_id, args):
    cart = args
    cart_items = cart.cart_items.filter(product_id=product_id)

    for cart_item in cart_items:
        # if multiple, only return the first instruction
        if cart_item.instructions:
            return cart_item.instructions

    return ""
