from django import forms
from .models import Order, Contact, Product


def get_mobile_form_field():
    return forms.TextInput(
        attrs={
            'type': 'tel',
            # allow spaces in mobile
            'pattern': '^(04\\d{2}\\s?\\d{3}\\s?\\d{3}|\\+61\\s?4\\d{2}\\s?\\d{3}\\s?\\d{3})$',
            'placeholder': '+614XXXXXXXX'
        }
    )


def get_home_phone_form_field():
    return forms.TextInput(
        attrs={
            'type': 'tel',
            # allow spaces in landline
            'pattern': '^0[2378]\\s?\\d{4}\\s?\\d{4}$',
            'placeholder': '08XXXXXXXX'
        }
    )


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
            'requested_delivery_date': forms.DateTimeInput(attrs={
                    'class': 'future-datetime-picker',
                    'type': 'datetime-local',
                    'step': 1800,  # 1800 seconds = 30 mins (30 min step increments)
                    # 'min': timezone.now().strftime('%d-%m-%YT%H:%M')
                },
                format='%d-%m-%YT%H:%M'  # exclude seconds
            ),
            'mobile': get_mobile_form_field(),
            'home_phone': get_home_phone_form_field()
        }


class ContactForm(ModelFormWithClassMixin, forms.ModelForm):
    class Meta:
        model = Contact
        products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(),
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
            'mobile': get_mobile_form_field(),
            'home_phone': get_home_phone_form_field()
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
