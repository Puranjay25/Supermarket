from django import forms

class CheckoutForm(forms.Form):
    items = forms.CharField(label='Enter Items', max_length=100, required=False)