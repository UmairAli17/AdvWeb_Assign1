from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddProductForm, ProductSearchForm, EditShopForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View, DetailView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import Product, Shop


# SHOP VIEWS

# the homepage for the website. it will show all the shops. uses the ListView CBV for displaying multiple objects
class IndexView(ListView):
    # the template to display all shop
    template_name = 'shop/index.html'
    # custom object for easier differentiation between object names
    context_object_name = 'shop_list'

    # gets all Shop objects from the Shop model (table)
    # def get_queryset is one of the views that we can override functions within CBV (Class-Based-Views)
    def get_queryset(self):
        return Shop.objects.all()

# the view that allows for the viewing a shop's details including any products it has. It uses the DetailView CBV for
# displaying a single object's details along with any related data that can be accessed through overriding the
# get_queryset or get_object methods - or in the template
class DetailView(DetailView):
    # use the shop model
    model = Shop
    # template to display the details
    template_name = 'shop/detail.html'

# the view that allows the user to access their own shop
class MyShopView(LoginRequiredMixin, DetailView):
    # the template that will display the current user's shop "profile"
    template_name = 'shop/my_shop.html'
    # custom object for the query. used in the foreach loop
    context_object_name = 'my_shop'

    # get the current user's shop and pass that into the object
    def get_object(self, queryset=None):
        # get the current user's shop
        user = self.request.user.id
        # get the user_shop where the owner is the current logged in user
        usr_shop = Shop.objects.get(owner=user)
        # return the above result
        return usr_shop

# the view that allows the user to edit their own shop
class EditMyShop(LoginRequiredMixin, UpdateView):
    # get the shop model
    model = Shop
    #the view will get the cuirrent user's shop through the id that is passed throught he url
    template_name = 'shop/edit_shop.html'
    # the formclass used for validation
    form_class = EditShopForm


# PRODUCT VIEWS

# Show ALL Products. CBV ListView for displaying multiple object models (results):
class AllProducts(ListView):
    # the model - it will allow for the listing of ALL products that have been uploaded by the users
    model = Product
    # the template that is used to display the products
    template_name = 'shop/all_products.html'

# create a product and assign the current logged in user.
class ProductCreate(LoginRequiredMixin, CreateView):
    # the model that will allow for the user to create a product
    model = Product
    # the form class that will run all the custom validation
    form_class = AddProductForm
    # the template where the form will be displayed
    template_name = 'shop/add_product.html'

    # if the form is valid then..
    def form_valid(self, form):
        # start a new product instance
        new_product = form.save(commit=False)
        # get current logged in user
        user = self.request.user.id
        # match the current logged in user to an owner in the Shop model.  this will get the primary for that row
        s = Shop.objects.get(owner=user)
        # assign the shop instance (id) to the product
        new_product.business = s
        # save the product to the database
        new_product.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(ProductCreate, self).form_valid(form)

# View that shows all the products the current user has added. Uses ListView CBV
class MyProducts(LoginRequiredMixin, ListView):
    # the template that is used to display the user's current products
    template_name = 'shop/my_products.html'
    # a custom name for the object for easier readability
    context_object_name = 'my_products'

    def get_queryset(self):
        # get the current logged in user's id
        user = self.request.user.id
        # run a query that searches for any product which belongs to a shop where the user is the owner
        queryset = Product.objects.filter(business__owner=user)
        # return results
        return queryset

# Shows the product details
class ProductDetailView(DetailView):
    # this will get the product model for that product so that it can be displayed
    model = Product
    template_name = 'shop/product_detail.html'

# All for the updating of products
class UpdateProduct(LoginRequiredMixin, UpdateView):
    # this will get the product model for that product so that it can be updated
    model = Product
    # specifies the template that the user will redirected to
    template_name = 'shop/product_form.html'
    # the fields that need to be displayed on the update product form
    fields = ['product_name', 'product_desc', 'price', 'product_image']


# Allows for the deleting of products. DeleteView is a CBV that allows for one to do this and to set a success url once
#  it is deleted
class DeleteProduct(LoginRequiredMixin, DeleteView):
    # this will get the product model for that product
    model = Product
    # once successfulyl deleted, redirect back to same page
    success_url = reverse_lazy('shop:my-products')

# The view that allows the user to search through a model which in this case is the Product model
class SearchList(ListView):
    # use the Product Model
    model = Product
    # set the formclass
    form_class = ProductSearchForm
    # the below template displays all results
    template_name = "shop/product_list_search.html"
    # set a custom object name
    context_object_name = 'search_list'

    # the following is what allows for the accessing of the value within the search box. it is a "get_queryset" as
    # we want to query the model depending on what the user has searched
    def get_queryset(self):
        # get the value from the search box
        search = self.request.GET.get("search")
        # if there is a value in the search box, run the below query.
        #  this is needed because I've set the search box required value to "False" in the form class
        if search:
            # the following query set will allow the user to search according to product name
            # distinct ensures that there are no duplicate entries
            # icontains gets a value
            queryset = Product.objects.filter(Q(product_name__icontains=search)).distinct
            return queryset
        else:
            # display an error message if they havent 
            messages.error(self.request, '')



