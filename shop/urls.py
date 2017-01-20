from django.conf.urls import url
from . import views, user_views

app_name = 'shop'


urlpatterns = [
    # the shop homepage
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # PRODUCT CRUD Functionality
    # Add the product to the user's shop
    # shop/product/add/
    url(r'^products/add/$', views.ProductCreate.as_view(), name='add-product'),

    # show the product
    # shop/products/all/
    url(r'^products/(?P<pk>[0-9]+)/$', views.ProductDetailView.as_view(), name="product-details"),

    # show ALL products
    # 'shop/products/all/'
    url(r'^products/all/', views.AllProducts.as_view(), name="all-products"),

    # Show my Products
    # 'shop/my-products'
    url(r'^my-products/', views.MyProducts.as_view(), name='my-products'),

    # update products
    # 'shop/product/1/edit/'
    url(r'^product/(?P<pk>[0-9]+)/edit/$', views.UpdateProduct.as_view(), name="update-product"),

    # Delete Product
    # 'shop/product/1/delete'
    url (r'^product/(?P<pk>[0-9]+)/delete/$', views.DeleteProduct.as_view(), name="delete-product"),

    # register user url
    # 'shop/register'
    url(r'^register/$', user_views.RegisterView.as_view(), name='register'),

    # logs user in
    # 'shop/login'
    url(r'^login/$', user_views.LoginView.as_view(), name='login'),
    
    # log the user out
    url(r'^logout/$', user_views.LogoutView.as_view(), name='logout'),

    # Show My Shop
    # 'shop/profile/'
    url(r'^shop/profile/$', views.MyShopView.as_view(), name='my-shop'),

    # Edit My Shop
    # 'shop/profile/1'
    url(r'^shop/profile/(?P<pk>[0-9]+)/$', views.EditMyShop.as_view(), name='edit-my-shop'),

    # Search Products
    url(r'^search/', views.SearchList.as_view(), name='search'),
]