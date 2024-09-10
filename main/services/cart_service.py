from ..models import Cart, Product


def get_cart(session_id, user_id=None):
    found_cart, created = Cart.objects.get_or_create(session_id=session_id)
    if created:
        found_cart.save()

    return found_cart


def add_product(cart_id, product_id, quantity: int):

    cart = Cart.objects.get(id=cart_id)

    if cart is None:
        raise ValueError("The cart is not found with id:" + cart_id)

    product = Product.objects.get(id=product_id)

    if product is None:
        raise ValueError("The product is undefined with id:" + product_id)
    elif quantity is None:
        raise ValueError("The quantity is not defined.")
    elif quantity != 0:
        cart_item, created = cart.cartitem_set.get_or_create(product=product,
                                                             defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity < 0:
                cart_item.delete()
            else:
                cart_item.save()


def update_quantity(cart_id, product_id, quantity: int):

    cart = Cart.objects.get(id=cart_id)

    if cart is None:
        raise ValueError("The cart is undefined")
    elif quantity is None:
        raise ValueError("The quantity is not defined.")

    product = Product.objects.get(id=product_id)

    if product is None:
        raise ValueError("The product is undefined with id:" + product_id)
    elif quantity == 0:
        # remove item out of cart
        cart_item = cart.cartitem_set.get(product=product)

        if cart_item is not None:
            cart_item.delete()
    elif quantity > 0:
        cart_item, created = cart.cartitem_set.get_or_create(product=product,
                                                             defaults={'quantity': quantity})
        if not created:
            cart_item.quantity = quantity
            cart_item.save()


def get_cart_items(cart_id):
    cart = Cart.objects.get(id=cart_id)
    return cart.cartitem_set.all()
