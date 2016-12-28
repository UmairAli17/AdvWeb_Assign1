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

    # register user url
    # 'music/register'
    #url(r'^register/$', views.RegisterView.as_view(), name='register'),

    # logs user in
    # 'music/login'
    url(r'^login/$', views.LoginView.as_view(), name='login'),

    # log the user out
    #url(r'^logout_user/$', .LogoutView.as_view(), name='logout_user'),

]