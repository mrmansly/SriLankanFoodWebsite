from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, ContactViewSet, ClassificationViewSet, ProductViewSet, FaqCategoryViewSet, FaqViewSet

from . import views

router = DefaultRouter()
router.register(r'cart-list', CartViewSet)
router.register(r'contact-list', ContactViewSet)
router.register(r'classification-list', ClassificationViewSet)
router.register(r'product-list', ProductViewSet)
router.register(r'faq-category-list', FaqCategoryViewSet)
router.register(r'faq-list', FaqViewSet)

urlpatterns = [
    path("", views.index_view, name="home"),
    path("products/", views.products_view, name="products"),
    path("cart/<int:cartId>", views.cart_view, name="cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("about/", views.about_view, name="about"),
    path("order/", views.order_view, name="order"),
    path("faq/", views.faq_view, name="faq"),
    path("contact/", views.contact_view, name="contact"),
    path("api-gateway/<str:api_path>", views.api_gateway_view, name='api_gateway'),
    path("contact-submitted/<str:contact_type>", views.contact_submitted_view, name="contact_submitted"),
    path('', include(router.urls))
]
