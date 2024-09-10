from django import forms
from .models import Order, Contact, Product


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'mobile', 'home_phone', 'requested_delivery_date']
        widgets = {
            'requested_delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(),
                                                 widget=forms.SelectMultiple,
                                                 required=True)
        fields = ['type', 'title', 'message', 'products', 'preferred_contact', 'response_required', 'email',
                  'mobile', 'home_phone', 'rating']
        widgets = {
            'products': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'response_required': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_contact': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'home_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['products'].required = False




