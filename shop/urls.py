from django.conf.urls import url
from . import views

app_name = 'shop'


urlpatterns = [
    # the shop homepage
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # PRODUCT CRUD Functionality
    # Add the product to the user's shop
    # shop/product/add/
    url(r'^product/add/$', views.ProductCreate.as_view(), name='add-product'),

    # show the product
    url(r'^product/(?P<pk>[0-9]+)/$', views.ProductDetailView.as_view(), name="product-details"),

    # show ALL products
    url(r'^pruducts/all/', views.AllProducts.as_view(), name="all-products"),

    # Show my Products
    url(r'^my-products/', views.MyProducts.as_view(), name='my-products'),

    # update products
    url(r'^product/(?P<pk>[0-9]+)/edit/$', views.UpdateProduct.as_view(), name="update-product"),

    # show the product
    url (r'^product/(?P<pk>[0-9]+)/delete/$', views.DeleteProduct.as_view(), name="delete-product"),

    # register user url
    # 'shop/register'
    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    # logs user in
    # 'shop/login'
    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # log the user out
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

]