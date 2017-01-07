from .forms import AddProductForm, ProductSearchForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View, DetailView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from .models import Product, Shop


# SHOP VIEWS

class IndexView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'shop_list'

    def get_queryset(self):
        return Shop.objects.all()


class DetailView(DetailView):
    model = Shop
    template_name = 'shop/detail.html'

class MyShopView(DetailView):
    template_name = 'shop/my_shop.html'
    context_object_name = 'my_shop'

    # get the current user's shop and pass that into the object
    def get_object(self, queryset=None):
        # get the current user's shop
        user = self.request.user.id
        usr_shop = Shop.objects.get(owner=user)
        return usr_shop

class EditMyShop(UpdateView):
    model = Shop
    template_name = 'shop/edit_shop.html'
    fields = ['name', 'description', 'shop_logo']



# PRODUCT VIEWS

# Show ALL Products:

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
    fields = ['product_name', 'product_desc', 'price', 'product_image']


class DeleteProduct(DeleteView):
    model = Product
    success_url = reverse_lazy('shop:my-products')


#function based view to search - will convert to CBV if needed - ok as is right now

class SearchList(ListView):
    model = Product
    form_class = ProductSearchForm
    template_name = "shop/product_list_search.html"
    context_object_name = 'search_list'

    def get_queryset(self):
        # get the value from the search box
        search = self.request.GET.get("search")
        # the following query set will allow the user to search according to product name
        queryset = Product.objects.filter(Q(product_name__icontains=search))
        return queryset


