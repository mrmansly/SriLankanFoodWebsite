from django.contrib import admin
from . models import Cart, CartItem, FaqCategory, Faq, User, Product, Order, OrderProduct, Classification, Contact, ContactType

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Classification)
admin.site.register(Contact)
admin.site.register(ContactType)
admin.site.register(FaqCategory)
admin.site.register(Faq)
