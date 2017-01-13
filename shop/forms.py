from django.contrib.auth.models import User
from .models import Product, Shop
from django.contrib.auth import authenticate
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

    def check_username(self):
        # get all current usernames withint he database
        user = User.objects.filter(username=self.cleaned_data['username'])
        # if the above user instance returns true then performt he following:
        if user:
            raise forms.ValidationError("That Username already exists! Please choose a different one.")
        return self.data['username']


    def clean(self, *args, **kwargs):
        self.check_username()
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

    # FUTURE DEV: Get the form authenticating user from here instead of within view. Quite messy as is right now
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     passsword = self.cleaned_data.get('passsword')
    #     # then we want ot authenticare (login the user)
    #     user = authenticate(username=username, passsword=passsword)
    #     if not user:
    #         raise forms.ValidationError("Incorrect login Credentials! Please try again!")
    #     return self.cleaned_data
    #
    # def login(self, request):
    #     username = self.cleaned_data.get('username')
    #     passsword = self.cleaned_data.get('passsword')
    #     user = authenticate(username=username, passsword=passsword)
    #     return user


class EditShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Shop Name','class': 'shop-formField'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Shop Description Here...', 'class': 'shop-formField'}),
        }
        exclude = ['owner']
        fields = ['name', 'description']



class AddProductForm(forms.ModelForm):
    product_image = forms.FileField(label="Upload a Product Image", required=True)
    price = forms.DecimalField(label="Please Enter A Price")
    class Meta:
        model = Product
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Enter Product Name', 'class': 'shop-formField'}),
            'product_desc': forms.Textarea(attrs={'placeholder': 'Enter Product Description Here...', 'class': 'shop-formField'}),
        }
        exclude = ['business', 'created']


class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False)