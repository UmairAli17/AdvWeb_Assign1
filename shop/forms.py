from django.contrib.auth.models import User
from .models import Product, Shop
from django import forms


class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a Password Here', 'class': 'shop-formField'}))
    conf_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password Here', 'class': 'shop-formField'}))

    # create the below function, this checks the currently submitted data and checks whether the password field matches the
    # confirm password field
    def clean_passwords(self):
        if self.cleaned_data['password'] != self.cleaned_data['conf_password']:
            raise forms.ValidationError("Your passwords do not match!")
        return self.data['password']

    def clean(self, *args, **kwargs):
        self.clean_passwords()
        return super(UserRegForm, self).clean()

    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter A Username Here', 'class': 'shop-formField'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter Your Email Here', 'class': 'shop-formField'}),
        }
        model = User
        fields = ['username', 'email', 'password']


class UserLogForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'shop-formField'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'shop-formField'}),
        }
        fields = ['username', 'password']

class AddProductForm(forms.ModelForm):
    product_image = forms.FileField(label="Upload a Product Image", required=True)
    class Meta:
        model = Product
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter Product Name', 'class': 'shop-formField'}),
            'product_desc': forms.Textarea(attrs={'placeholder': 'Enter Product Description Here...', 'class': 'shop-formField'}),
        }
        exclude = ['business']