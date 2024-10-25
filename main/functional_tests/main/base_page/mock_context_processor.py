from unittest.mock import Mock
from django.db.models.query import QuerySet

def mocked_cart_context(request):
    return {
        'cart_items': 1
    }

# the existence of some data is all that is needed for this mock
def mocked_product_stock_context(request):

    mock_queryset = Mock(spec=QuerySet)
    mock_data = [
        Mock()
    ]
    mock_queryset.all.return_value = []

    return {
        'product_stock': mock_queryset
    }