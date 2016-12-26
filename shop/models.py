from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Shop Model. A Shop Object will be created when the user registers
class Shop(models.Model):
    name = models.CharField(max_length=150)
    owner = models.OneToOneField(User)
    shop_logo = models.FileField()

    def __str__(self):
        return self.name


# The class that will link a product to the user
class Products(models.Model):
    product_name = models.CharField(max_length=250)
    # connect the product to the shop
    business = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product_desc = models.TextField()
    product_image = models.FileField()

    def __str__(self):
        return self.name

    # a future fucntion that will allow for the viewing of a shop
    #def get_absolute_url(self):
    #    return reverse('shop:detail', kwargs={'pk': self.pk})