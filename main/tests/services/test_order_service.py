from django.test import TestCase
from main.models import Cart, Order, ProductStock, Product, OrderProduct
from main.fixtures.fixture_loader_utils import load_sample_cart, load_sample_order
from main.services.order_service import save_order_products


class TestOrderService(TestCase):

    def setUp(self):
        load_sample_cart()
        load_sample_order()

    def test_save_order_products_with_remaining_stock_decrement(self):

        self.prepare_for_save_order_products()
        ProductStock.objects.create(product=self.product, quantity=3)
        save_order_products(self.order, self.cart_items)

        self.verify_order_product_saved()

        # verify that product stock decremented correctly
        product_stock = ProductStock.objects.get(product=self.product)
        self.assertEqual(product_stock.quantity, 2)

    def test_save_order_products_with_more_stock_decrement_than_available(self):

        self.prepare_for_save_order_products()
        ProductStock.objects.create(product=self.product, quantity=0)
        save_order_products(self.order, self.cart_items)

        self.verify_order_product_saved()

        # verify that product stock decremented correctly by not putting it into -ve
        product_stock = ProductStock.objects.get(product=self.product)
        self.assertEqual(product_stock.quantity, 0)

    def test_save_order_products_with_missing_stock_decrement(self):
        self.prepare_for_save_order_products()
        save_order_products(self.order, self.cart_items)
        self.verify_order_product_saved()

    def prepare_for_save_order_products(self):
        self.product = Product.objects.get(id=2)
        self.order = Order.objects.get(id=1)
        self.cart = Cart.objects.get(id=1)
        self.cart_items = self.cart.cart_items.all()

    def verify_order_product_saved(self):
        # verify that order item is saved
        order_product = OrderProduct.objects.get(order=self.order, product=self.product)
        self.assertIsNotNone(order_product)

