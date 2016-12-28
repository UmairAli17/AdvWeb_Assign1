from django.contrib.auth.models import User
from .models import Product, Shop
from django import forms

class UserLogForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password']

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_desc', 'product_image']
        exclude = ['business']
