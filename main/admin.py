from django.contrib import admin
from . models import Cart, CartItem, FaqCategory, Faq, Product, Order, OrderProduct, Classification, Contact, \
    ContactType, SystemPreference, ProductStock, EmailConfiguration


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderProduct._meta.fields]


class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields]


class CartItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CartItem._meta.fields]


# Register your models here.
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Classification)
admin.site.register(Contact)
admin.site.register(ContactType)
admin.site.register(FaqCategory)
admin.site.register(Faq)
admin.site.register(SystemPreference)
admin.site.register(ProductStock)
admin.site.register(EmailConfiguration)
