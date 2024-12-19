from django import forms
from .models import ShippingAdress
from phonenumber_field.formfields import PhoneNumberField

from phonenumber_field.formfields import PhoneNumberField
class ShippingForm(forms.ModelForm):
    Shipping_full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder':'Full name'}),required=True)
    Shipping_email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Email'}),required=False)
    Shipping_addresse = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Address'}),required=True)
    Shipping_city = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'City'}),required=True)
    Shipping_zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Zipcode'}),required=False)
    # shipping_numberphone=forms.PhoneNumberField(max_length=10,label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Numero de telephone'}),required=True)
    shipping_numberphone =forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','type': 'tel','placeholder': 'Numero de telephone'}),required=False)

    class Meta:
        model = ShippingAdress
        fields = ['Shipping_full_name', 'Shipping_email', 'Shipping_addresse', 'Shipping_city', 'Shipping_zipcode','shipping_numberphone']
        exclude=["user"]


 

class PaymentForm(forms.Form):
	card_name=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Nom de carte'}),required=True)
	card_number=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Numero de carte'}),required=True)
	card_exp_date=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Date dexpiration '}),required=True)
	card_cvv=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'carte cvv'}),required=True)
	card_adress=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Address carte'}),required=True)
	number_phone=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Numero telephone'}),required=True)