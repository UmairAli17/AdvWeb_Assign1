from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddProductForm, ProductSearchForm, EditShopForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Product, Shop


# SHOP VIEWS

# LoginRequiredMixin
# Allows only authenticated (logged in users) to access the view(s)

# the homepage for the website. it will show all the shops. uses the ListView CBV for displaying multiple objects
class IndexView(ListView):
    model = Shop
    template_name = 'shop/index.html'
    context_object_name = 'shop_list'

# Show the shop's details 
class DetailView(DetailView):
    # Attach the product model to this View
    model = Shop
    template_name = 'shop/detail.html'

# the view that allows the user to access their own shop
class MyShopView(LoginRequiredMixin, DetailView):
    template_name = 'shop/my_shop.html'
    context_object_name = 'my_shop'

    # get the current user's shop and pass that into the object
    def get_object(self, queryset=None):
        # get the current user's shop
        user = self.request.user.id
        # get the user_shop where the owner is the current logged in user
        usr_shop = Shop.objects.get(owner=user)
        return usr_shop

# the view that allows the user to edit their own shop
class EditMyShop(LoginRequiredMixin, UpdateView):
    model = Shop
    template_name = 'shop/edit_shop.html'
    form_class = EditShopForm


# PRODUCT VIEWS

# show all products, uploaded by all users (shop owners)
class AllProducts(ListView):
    # Attach the product model to this View
    model = Product
    template_name = 'shop/all_products.html'

# create a product and assign the current logged in user.
class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'shop/add_product.html'

    # if the form is valid then..
    def form_valid(self, form):
        new_product = form.save(commit=False)
        # get current logged in user
        user = self.request.user.id
        # match the current logged in user to an owner in the Shop model.  this will get the primary for that row
        s = Shop.objects.get(owner=user)
        # assign the shop instance (id) to the product
        new_product.business = s
        # save the product to the database
        new_product.save()
        return super(ProductCreate, self).form_valid(form)

# View that shows all the products the current user has added. Uses ListView CBV
class MyProducts(LoginRequiredMixin, ListView):
    template_name = 'shop/my_products.html'
    context_object_name = 'my_products'

    def get_queryset(self):
        user = self.request.user.id
        # run a query that searches for any product which belongs to a shop where the user is the owner
        queryset = Product.objects.filter(business__owner=user)
        return queryset

# Shows the product details
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

# All for the updating of products
class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'shop/product_form.html'
    fields = ['product_name', 'product_desc', 'price', 'product_image']


# Allows for the deleting of products. DeleteView is a CBV that allows for one to do this and to set a success url once
#  it is deleted so that the user is sent to whatever page is defined within the "success_url"
class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('shop:my-products')

# The view that allows the user to search through a model which in this case is the Product model
class SearchList(ListView):
    model = Product
    form_class = ProductSearchForm
    template_name = "shop/product_list_search.html"
    context_object_name = 'search_list'

    # the following is what allows for the accessing of the value within the search box. it is a "get_queryset" as
    # query the Product model depending on what the user has searched for
    def get_queryset(self):
        search = self.request.GET.get("search")
        # if there is a value in the search box, run the below query.
        if search:
            # the following query set will allow the user to search according to product name - distinict will ensure there are no duplicate results
            queryset = Product.objects.filter(Q(product_name__icontains=search)).distinct
            return queryset
        else:
            messages.error(self.request, '')



