from django import forms
from .models import Order, Contact, Product


class ModelFormWithClassMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if type(field.widget) is not forms.CheckboxInput:
                # Add a CSS class to each widget
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'


class CheckoutForm(ModelFormWithClassMixin, forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'mobile', 'home_phone', 'requested_delivery_date']
        widgets = {
            'requested_delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ContactForm(ModelFormWithClassMixin, forms.ModelForm):
    class Meta:
        model = Contact
        product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(),
                                                 widget=forms.SelectMultiple,
                                                 required=True)
        fields = ['type', 'title', 'message', 'products', 'preferred_contact', 'response_required', 'email',
                  'mobile', 'home_phone', 'rating']
        widgets = {
            'products': forms.SelectMultiple(),
            'response_required': forms.CheckboxInput(),
            'type': forms.Select(),
            'preferred_contact': forms.Select(),
            'rating': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['products'].required = False




