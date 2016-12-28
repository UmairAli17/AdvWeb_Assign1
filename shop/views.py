from django.views import generic
from .forms import UserLogForm, AddProductForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from .models import Product, Shop


# SHOP VIEWS

class IndexView(ListView):
    template_name = 'shop/index.html'
    context_object_name = 'shop_list'

    def get_queryset(self):
        return Shop.objects.all()


class DetailView(generic.DetailView):
    model = Shop
    template_name = 'shop/detail.html'



# PRODUCT VIEWS


class ProductCreate(CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'shop/add-product.html'

    def form_valid(self, form):
        form.save(commit=False)
        # get current logged in user
        user = self.request.user.id
        # match the current logged in user to an owner in the Shop model
        s = Shop.objects.get(owner=user)
        # get the id of that owner's shop identification number
        form.business = s.id
        form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(ProductCreate, self).form_valid(form)



class LoginView(generic.View):
    form_class = UserLogForm
    template_name = 'shop/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # wrap the form text boxes in variables
        username = request.POST['username']
        password = request.POST['password']
        # assign a variable to the function that authenticates the user
        user = authenticate(username=username, password=password)

        # if the user exists
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/shop/')
            else:
                # if user is not active, ask to logon again
                return HttpResponseRedirect('/shop/login')

        return HttpResponseRedirect('/shop/login')