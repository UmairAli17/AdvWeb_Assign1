from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Shop Model Class. A Shop Object will be created when the user registers.
# It will allow the user to add products to their shop
class Shop(models.Model):
    name = models.CharField(max_length=150)
    # connect the owner to a user in django's default User model and set to a one-to-one relationship as each user will have ONE shop
    owner = models.OneToOneField(User, related_name="owner")
    description = models.TextField(max_length=5000, default="Default Description. Looks like the Shop Owner hasn't uploaded a description..")

    def __str__(self):
        return str(self.id)

    # this will create a shop when a user registers. It uses the post_save signal when a new user instance is initiated
    def create_shop(sender, **kwargs):
        # get the User model created signal instance that's initiated on user being created
        user = kwargs["instance"]
        if kwargs["created"]:
            # set the newly created (registered) user's id as the Shop model's Owner column value. This will connect a Shop to 
            # the newly created user
            up = Shop(owner=user)
            up.save()
    # the post_save signal that tells the User model that after the User model's "created" (user regisration) 
    # instance has been initiated, to create a shop Model object by running the above "create_shop" function 
    post_save.connect(create_shop, sender=User)

    # redirect user to the user's product page upon successfully updating the user's shop
    def get_absolute_url(self):
        return reverse('shop:my-shop')


# The Model Class for storing Products for the Users' Shops
class Product(models.Model):
    product_name = models.CharField(max_length=250)
    # connect the product to the shop using one to many - a shop can have multiple products
    business = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    product_desc = models.TextField()
    product_image = models.FileField()
    # decimal fields will allow for allowing the user to add pences to their product pricing.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # auto_now_add gets the current date and time of when the product was created
    created = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return self.product_name

    # a function that will allow for the viewing of a product upon successfully updating a product
    def get_absolute_url(self):
        return reverse('shop:product-details', kwargs={'pk': self.pk})

    # a custom attribute that formats the price of the product so that there us a £ before the value - called primarily in templates.
    @property
    def price_format(self):
        return "£%s" % self.price
