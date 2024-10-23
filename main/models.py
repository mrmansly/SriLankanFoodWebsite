from django.db import models
from django.utils import timezone
from .enums import ContactNotificationTypeEnum, ContactTypeEnum
from django.core.exceptions import ValidationError
from .services.phone_validation_service import validate_mobile, validate_landline


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=20, null=True)
    home_phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"Username {self.user_name}: {self.first_name} {self.last_name}"


class Classification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"Classification {self.name} (Order:{self.order}): {self.description}"


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)
    image = models.CharField(null=True, max_length=100)
    chilli_level = models.IntegerField(null=True)
    contains_peanuts = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


# A cart can ONLY be associated to one user or session id.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    # Used if there is no associated user logged in at the time
    session_id = models.CharField(null=True, max_length=40, blank=True, unique=True)

    def clean(self):
        if self.user is None and self.session_id is None:
            raise ValueError("Cart cannot be created without a user or session id reference.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        string_result = f"Cart {self.id}"
        if self.user is not None:
            string_result += f" belongs to {self.user.user_name}"
        return string_result


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    instructions = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} item(s) of {self.product.name} exist in Cart {self.cart.id}"


class Order(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(max_length=320)
    mobile = models.CharField(max_length=20, null=True)
    home_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Home Phone")
    discount = models.FloatField(default=0)
    total_price = models.FloatField()
    requested_delivery_date = models.DateTimeField(null=True, verbose_name="Delivery Date")
    created_date = models.DateTimeField(default=timezone.now)
    completed_date = models.DateTimeField(null=True, blank=True)
    confirmation_sent_date = models.DateTimeField(null=True, blank=True, db_index=True)
    cancelled_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id}: created on {self.created_date}"

    def clean(self):
        self.mobile = validate_mobile(self.mobile)
        self.home_phone = validate_landline(self.home_phone)
        self.validate_requested_delivery_date()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # validate that the requested delivery date is a future date
    def validate_requested_delivery_date(self):
        if self.requested_delivery_date < timezone.now():
            raise ValidationError("Requested Delivery Date must be a future date.")


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    instructions = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.quantity} item(s) of {self.product.name} belonging to Order {self.order.id}"


class ProductStock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} item(s) of {self.product.name} currently in stock"


class FaqCategory(models.Model):
    category = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.category}"


class Faq(models.Model):
    question = models.CharField(max_length=100, unique=True)
    answer = models.TextField(max_length=1000)
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.id} - {self.question}"


class ContactType(models.Model):
    type = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} - {self.type}"


class Contact(models.Model):
    CONTACT_METHOD_CHOICES = [
        (ContactNotificationTypeEnum.EMAIL.value, 'Email'),
        (ContactNotificationTypeEnum.MOBILE.value, 'Mobile'),
        (ContactNotificationTypeEnum.HOME_PHONE.value, 'Home Phone')
    ]

    type = models.ForeignKey(ContactType, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    response_required = models.BooleanField(default=False)
    preferred_contact = models.CharField(max_length=20, null=True, choices=CONTACT_METHOD_CHOICES,
                                         default=ContactNotificationTypeEnum.EMAIL.value, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    home_phone = models.CharField(max_length=20, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='contacts', blank=True)

    RATINGS_CHOICES = [
        # (None, 'No Selection'),
        (0, 'No Stars - Worst food ever!'),
        (1, '1 Star - I wish I had spent that money elsewhere'),
        (2, '2 Stars - Food was edible, but won''t be coming back'),
        (3, '3 Stars - Was nice but nothing out of the ordinary'),
        (4, '4 Stars - Pretty, pretty, pretty good'),
        (5, '5 Stars - Oooh la la - Restaurant Quality')
    ]
    # Value from 0 to 5 (0 being the worst and 5 being the best)
    rating = models.PositiveSmallIntegerField(choices=RATINGS_CHOICES, default=None, null=True, blank=True)

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.type}: {self.title} - {self.message}"

    def clean(self):
        if self.response_required:
            if self.preferred_contact == ContactNotificationTypeEnum.EMAIL.value and self.email is None:
                raise ValidationError("A valid email is required so we can respond back")
            if self.preferred_contact == ContactNotificationTypeEnum.MOBILE.value and self.mobile is None:
                raise ValidationError('A valid mobile is required so we can respond back')
            if self.preferred_contact == ContactNotificationTypeEnum.HOME_PHONE.value and self.home_phone is None:
                raise ValidationError('A valid home phone is required so we can respond back')

        if self.type_id == ContactTypeEnum.REVIEW.value and self.rating is None:
            raise ValidationError('A rating is required when submitting a Food Review')

        self.mobile = validate_mobile(self.mobile)
        self.home_phone = validate_landline(self.home_phone)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SystemPreference(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=50)
    value = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}:{self.value}"
