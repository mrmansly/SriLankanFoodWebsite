from ..models import Cart, Product


def get_cart(session_id, user_id=None):
    found_cart, created = Cart.objects.get_or_create(session_id=session_id)
    if created:
        found_cart.save()

    return found_cart


def add_product(cart_id, product_id, quantity: int, instructions):

    cart = Cart.objects.get(id=cart_id)

    if cart is None:
        raise ValueError("The cart is not found with id:" + cart_id)

    product = Product.objects.get(id=product_id)

    if product is None:
        raise ValueError("The product is undefined with id:" + product_id)
    elif quantity is None:
        raise ValueError("The quantity is not defined.")
    elif quantity > 0:
        cart_item, created = cart.cart_items.get_or_create(product=product,
                                                             defaults={'quantity': quantity,
                                                                       'instructions': instructions})

        if not created:
            cart_item.quantity = quantity
            cart_item.instructions = instructions
            cart_item.save()
    else:

        # Cater for the scenario where a -ve quantity is passed through from the client and no cart item
        # matching that product is found.
        cart_items = cart.cart_items.filter(product=product)

        if cart_items.count() == 1:
            cart_items[0].delete()


# instructions - if "None" passed in then keep existing instructions
def update_cart_details(cart_id, product_id, quantity: int, instructions=None):

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
        cart_item = cart.cart_items.get(product=product)

        if cart_item is not None:
            cart_item.delete()
    elif quantity > 0:

        defaults = {'quantity': quantity}

        if instructions is not None:
            defaults['instructions'] = instructions

        cart_item, created = cart.cart_items.get_or_create(product=product,
                                                             defaults=defaults)
        if not created:
            cart_item.quantity = quantity
            if instructions is not None:
                cart_item.instructions = instructions

            cart_item.save()


def get_cart_items(cart_id):
    cart = Cart.objects.get(id=cart_id)
    return cart.cart_items.all()
