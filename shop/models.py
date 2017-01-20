from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.


# Shop Model. A Shop Object will be created when the user registers
class Shop(models.Model):
    name = models.CharField(max_length=150)
    # connect the owner to a user int he User model
    owner = models.OneToOneField(User, related_name="owner")
    # textfields allow for the use of "textareas".
    description = models.TextField(max_length=5000, default="Default Description. Looks like the Shop Owner hasn't uploaded a description..")

    def __str__(self):
        return str(self.id)

    # this will create a shop when a user registers

    def create_shop(sender, **kwargs):
        # get the User mnodel created signal - when user is created, get that instance
        user = kwargs["instance"]
        # if the kwargs is of a created instance:
        if kwargs["created"]:
            # set the owner column value to whatever has been obtained from the created user instance
            # if user "Ben" registers, set owner value to "ben"
            up = Shop(owner=user)
            # save this owner to database
            up.save()
    # this is the signal that tells django that after the User model (row/object) has been created, run the function
    post_save.connect(create_shop, sender=User)

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
    # decimal fields will allow for allowing the user to add pences to their product pricing.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # auto_now_add gets the current date and time of when the product was created
    created = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return self.product_name


    # method that appends a £ sign before the price value in the template
    # a  function that will allow for the viewing of a product
    def get_absolute_url(self):
        return reverse('shop:product-details', kwargs={'pk': self.pk})

    # a custom attribute that formats the price of the product so that there us a £ before the value.
    @property
    def price_format(self):
        return "£%s" % self.price
