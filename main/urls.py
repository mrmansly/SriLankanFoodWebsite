from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.api_views import (CartViewSet, ContactViewSet, ClassificationViewSet, ProductViewSet, FaqCategoryViewSet,
                              FaqViewSet, ContactTypeViewSet, OrderViewSet)

from .views import web_views, api_views

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'contact-types', ContactTypeViewSet, basename='contact-type')
router.register(r'classifications', ClassificationViewSet, basename='classification')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'faq-categories', FaqCategoryViewSet, basename='faq-category')
router.register(r'faqs', FaqViewSet, basename='faq')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path("", web_views.index_view, name="home"),
    path("menu/", web_views.menu_view, name="menu"),
    path("checkout/", web_views.checkout_view, name="checkout"),
    path("about/", web_views.about_view, name="about"),
    path("order/", web_views.order_view, name="order"),
    path("faq/", web_views.faq_view, name="faq"),
    path("contact/", web_views.contact_view, name="contact"),
    path("api/update-cart-item-quantity", api_views.CartItemQuantityUpdateView.as_view(), name='update_cart_item_api'),
    path("contact-submitted/<str:contact_type>", web_views.contact_submitted_view, name="contact_submitted"),
    # api specific paths
    path('api/', include(router.urls))
]
