from django.contrib.auth.models import User
from .models import Product, Shop
from django import forms


class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput(), label="Please Confirm Your Password")

    # create the below function, this checks the currently submitted data and checks whether the password field matches the
    # confirm passwoprd field
    def clean_passwords(self):
        if self.cleaned_data['password'] != self.cleaned_data['conf_password']:
            raise forms.ValidationError("Your passwords do not match!")
        return self.data['password']

    def clean(self, *args, **kwargs):
        self.clean_passwords()
        return super(UserRegForm, self).clean()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


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
