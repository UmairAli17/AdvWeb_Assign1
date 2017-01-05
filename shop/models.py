from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.


# Shop Model. A Shop Object will be created when the user registers
class Shop(models.Model):
    name = models.CharField(max_length=150)
    owner = models.OneToOneField(User, related_name="owner")
    shop_logo = models.FileField()

    def __str__(self):
        return str(self.id)

    def create_shop(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            up = Shop(owner=user)
            up.save()
    post_save.connect(create_shop, sender=User)

    @property
    def shop_logo_img(self):
        default_path = '/static/shop/images/dft/no-img.png'
        if self.shop_logo:
            return self.shop_logo.url
        else:
            return default_path

    # redirect user to the user's product page
    def get_absolute_url(self):
        return reverse('shop:my-products')


# The class that will link a product to the shop
class Product(models.Model):
    product_name = models.CharField(max_length=250)
    # connect the product to the shop
    business = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    product_desc = models.TextField()
    product_image = models.FileField()

    def __str__(self):
        return self.product_name


# a  function that will allow for the viewing of a product
    def get_absolute_url(self):
        return reverse('shop:product-details', kwargs={'pk': self.pk})
