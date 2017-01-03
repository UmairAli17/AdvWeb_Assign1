from django.views import generic
from .forms import UserLogForm, AddProductForm, UserRegForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from .models import Product, Shop


# SHOP VIEWS

class IndexView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'shop_list'

    def get_queryset(self):
        return Shop.objects.all()


class DetailView(generic.DetailView):
    model = Shop
    template_name = 'shop/detail.html'

# PRODUCT VIEWS

# Show ALL Products

class AllProducts(ListView):
    model = Product
    template_name = 'shop/all_products.html'


class ProductCreate(CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'shop/add_product.html'

    def form_valid(self, form):
        new_product = form.save(commit=False)
        # get current logged in user
        user = self.request.user.id
        # match the current logged in user to an owner in the Shop model.  this will get the primary for that row
        s = Shop.objects.get(owner=user)
        # assign the shop instance (id) to the product
        new_product.business = s
        new_product.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(ProductCreate, self).form_valid(form)


class MyProducts(ListView):
    template_name = 'shop/my_products.html'
    context_object_name = 'my_products'

    def get_queryset(self):
        user = self.request.user.id
        queryset = Product.objects.filter(business__owner=user)
        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

# All for the updating of products
class UpdateProduct(UpdateView):
    model = Product
    template_name = 'shop/product_form.html'
    fields = ['product_name', 'product_desc', 'product_image']


class DeleteProduct(DeleteView):
    model = Product
    success_url = reverse_lazy('shop:my-products')


# USER AUTH VIEWS


class RegisterView(CreateView):
     form_class = UserRegForm
     template_name = 'shop/registration_form.html'

     #display the template when this view is called - when the user requests the page itself
     def get(self, request):
         #display the form - None ensures that there won't be any data in it.. yet
         form = self.form_class(None)
         return render(request, self.template_name, {'form': form})

     def post(self, request):
         form = self.form_class(request.POST)

         if form.is_valid():
             user = form.save(commit=False)

             username = form.cleaned_data['username']
             password = form.cleaned_data['password']

             user.set_password(password)
             user.save()

             user = authenticate(username=username, password=password)

             if user is not None:
                 if user.is_active:
                     login(request, user)
                     return HttpResponseRedirect('/shop/')
                 else:
                     return HttpResponseRedirect('/shop/')

         return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = UserLogForm
    template_name = 'shop/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # wrap the form text boxes in variables
        username = request.POST['username']
        password = request.POST['password']
        # assign a variable to the function that authenticates the user
        user = authenticate(username=username, password=password)

        # if the user exists
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/shop/')
            else:
                # if user is not active, ask to logon again
                return HttpResponseRedirect('/shop/login')

        return HttpResponseRedirect('/shop/login')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/shop/')
