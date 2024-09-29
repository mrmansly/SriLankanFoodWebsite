# The GST Rate (hardcoded for now)
GST_RATE = 10

DEFAULT_DISCOUNT = 0


# Return the total price of the order (inclusive of GST and Discounts)
# Discount functionality not yet added
def get_total_price(item_list):
    total_price = 0

    if item_list is not None:
        net_price = get_net_cost(item_list)
        total_gst = get_gst(item_list)
        total_discount = get_discount()

        total_price = net_price - total_discount + total_gst

    return total_price


def get_discount():
    return DEFAULT_DISCOUNT


# Return the total net cost of the order (excluding GST)
def get_net_cost(item_list):
    net_price = 0

    if item_list is not None:
        for item in item_list:
            net_price += item.quantity * item.product.price

    return net_price


# Return the GST amount of the order
# Discount functionality not yet added
def get_gst(item_list):

    total_gst = 0

    if item_list is not None:
        net_price = get_net_cost(item_list)

        if net_price > 0:
            total_gst = (net_price - get_discount()) / GST_RATE

    return total_gst


# Return an object containing total, net and GST prices
def get_all_price_data(item_list):
    total_price = get_total_price(item_list)
    net_cost = get_net_cost(item_list)
    gst = get_gst(item_list)
    discount = get_discount()
    revised_net_cost = net_cost - discount
    return {
        "total_price": total_price,
        "net_cost": net_cost,
        "gst": gst,
        "discount": discount,
        "revised_net_cost": revised_net_cost
    }
