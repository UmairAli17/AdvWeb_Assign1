from django.conf.urls import url
from . import views

app_name = 'shop'


urlpatterns = [
    # the shop homepage
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # PRODUCT CRUD Functionality
    # Add the product to the user's shop
    # music/album/add/
    url(r'^album/add/$', views.ProductCreate.as_view(), name='product-add'),


    # Show my Products
    url(r'^my-products/$', views.MyProducts.as_view(), name='my-products'),

    # register user url
    # 'shop/register'
    url(r'^register/$', views.RegisterView.as_view(), name='register'),

    # logs user in
    # 'shop/login'
    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # log the user out
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

]