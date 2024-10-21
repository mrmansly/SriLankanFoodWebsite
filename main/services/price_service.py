from .system_preference_service import get_value, is_enabled
from ..enums import SystemPreferenceName

# To be handled as a future task.  For now there is no discount functionality
DEFAULT_DISCOUNT = 0


def get_gst_rate():
    return get_value(SystemPreferenceName.GST_RATE.value)


def is_gst_enabled():
    return is_enabled(SystemPreferenceName.GST_ENABLED.value)


# Return the total price of the order (inclusive of GST and Discounts)
# Discount functionality not yet added
def get_total_price(item_list):
    total_price = 0

    if item_list:
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

    if item_list:
        for item in item_list:
            net_price += item.quantity * item.product.price

    return net_price


# Return the GST amount of the order
# Discount functionality not yet added
def get_gst(item_list):

    total_gst = 0

    if item_list and is_gst_enabled():

        net_price = get_net_cost(item_list)

        if net_price > 0:
            total_gst = (net_price - get_discount()) / get_gst_rate()

    return total_gst


# Return an object containing total, net and GST prices
def get_all_price_data(item_list):
    total_price = get_total_price(item_list)
    net_cost = get_net_cost(item_list)
    gst = get_gst(item_list)
    discount = get_discount()
    revised_net_cost = net_cost - discount
    gst_enabled = is_gst_enabled()
    return {
        "total_price": total_price,
        "net_cost": net_cost,
        "gst": gst,
        "gst_enabled": gst_enabled,
        "discount": discount,
        "revised_net_cost": revised_net_cost
    }
