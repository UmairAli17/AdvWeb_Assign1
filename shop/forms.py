from django.contrib.auth.models import User
from .models import Product, Shop
from django.contrib.auth import authenticate
from django import forms


class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a Password Here', 'class': 'shop-formField'}))
    conf_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password Here', 'class': 'shop-formField'}))

    # create the below function, this checks the currently submitted data and checks whether the password field
    # matches the confirm password field
    def clean_passwords(self):
        # get values from password field and the conf_password field.
        # if the values arent the same, then raise an error
        if self.cleaned_data['password'] != self.cleaned_data['conf_password']:
            raise forms.ValidationError("Your passwords do not match!")
        # else if it's matching, send the password along
        return self.data['password']

    #check whether username is unique within the database
    def check_username(self):
        # get all current usernames withint he database and then look for a user name that matches whatever has been sent through the form
        user = User.objects.filter(username=self.cleaned_data['username'])
        # if the above user instance returns true then perform the following:
        # if the above query gets a result, raise a val error
        if user:
            raise forms.ValidationError("That Username already exists! Please choose a different one.")
        # else if the username they've entered is valid then send along the username
        return self.data['username']

    # the clean method is what the form runs as part of the form class
    def clean(self, *args, **kwargs):
        # the two custom functions have been called here on the clean to ensure theya re run.
        self.check_username()
        self.clean_passwords()
        return super(UserRegForm, self).clean()

    # defines how fields should be displayed
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter A Username Here', 'class': 'shop-formField'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter Your Email Here', 'class': 'shop-formField'}),
        }
        # the registration form uses Django's User model
        model = User
        # ensures the following fields are outputted from the model
        fields = ['username', 'email', 'password']


# User Login form
class UserLogForm(forms.ModelForm):
    class Meta:
        # uses the user model
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'shop-formField'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'shop-formField'}),
        }
        fields = ['username', 'password']


# the editing shop form. allows for the editing of shop
class EditShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Shop Name','class': 'shop-formField'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Shop Description Here...', 'class': 'shop-formField'}),
        }
        # exclude ensures that the owner field doesn't come up. owner will be set through the View function
        exclude = ['owner']
        fields = ['name', 'description']


# the form class that will allow for adding products
class AddProductForm(forms.ModelForm):
    product_image = forms.FileField(label="Upload a Product Image", required=True)
    price = forms.DecimalField(label="Please Enter A Price")
    class Meta:
        # uses product model
        model = Product
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter Product Name', 'class': 'shop-formField'}),
            'product_desc': forms.Textarea(attrs={'placeholder': 'Enter Product Description Here...', 'class': 'shop-formField'}),
        }
        exclude = ['business', 'created']


# the formclass for the search bar.
class ProductSearchForm(forms.Form):
    # required is false so to make sure that a "required" error doesn't appear on every page
    search = forms.CharField(required=False)




