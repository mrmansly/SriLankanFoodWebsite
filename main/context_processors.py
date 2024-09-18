from main.models import Cart


def cart_context(request):
    cart = get_cart(request)
    cart_items = get_cart_items(cart)

    return {
        'cart': cart,
        'cart_items': cart_items
    }


def get_cart(request):
    if request.session is None:
        return None
    else:
        cart_obj, created = Cart.objects.get_or_create(session_id=request.session.session_key)
        return cart_obj


def get_cart_items(cart: Cart):
    count = 0
    if cart is not None:
        for item in cart.cart_items.all():
            count += item.quantity

    return count

