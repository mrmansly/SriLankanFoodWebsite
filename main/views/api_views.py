from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..services.cart_service import add_product
from rest_framework import viewsets
from ..serializers import CartSerializer, ContactSerializer, ProductSerializer, ClassificationSerializer, \
    ContactTypeSerializer, FaqCategorySerializer, FaqSerializer, OrderSerializer, CartItemQuantityUpdateSerializer
from main.models import Cart, Contact, Faq, FaqCategory, Product, Classification, ContactType, Order
from django_filters import rest_framework as filters


class CartItemQuantityUpdateView(APIView):

    # For now, allow anyone to call this API as user may not have a login at this point
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CartItemQuantityUpdateSerializer(data=request.data)
        if serializer.is_valid():
            if self.validate_request_matches_with_cart(serializer.validated_data['cart_id'], request):
                # Process the data
                add_product(
                    serializer.validated_data['cart_id'],
                    serializer.validated_data['product_id'],
                    serializer.validated_data['quantity'],
                    serializer.validated_data.get('instructions')
                )
                return Response(self.get_serialized_cart(serializer.validated_data['cart_id']), status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid cart or session mismatch."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Validate that the user's request matches with the cart they are trying to update.
    def validate_request_matches_with_cart(self, cart_id, request) -> bool:
        # first check carts belonging to the user as the session may have expired
        cart = None
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user_id=request.user.id, id=cart_id)

        if cart is None:
            # check on session instead (assuming session has not expired from when cart was first created)
            cart = Cart.objects.filter(session_id=request.session.session_key, id=cart_id)

        if not cart:
            return False

        return True

    def get_serialized_cart(self, cart_id):
        cart = Cart.objects.prefetch_related('cart_items').get(id = cart_id)
        cart_serializer = CartSerializer(cart, many=False)
        return cart_serializer.data


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer


class ContactTypeViewSet(viewsets.ModelViewSet):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class FaqCategoryViewSet(viewsets.ModelViewSet):
    queryset = FaqCategory.objects.all()
    serializer_class = FaqCategorySerializer


class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        method='filter_by_status'
    )

    class Meta:
        model = Order
        fields = []

    def filter_by_status(self, queryset, name, value):
        if value == 'active':
            return queryset.filter(completed_date__isnull=True, cancelled_date__isnull=True)
        elif value == 'completed':
            return queryset.filter(completed_date__isnull=False)
        elif value == 'cancelled':
            return queryset.filter(cancelled_date__isnull=False)

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
