from .forms import UserLogForm, UserRegForm
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect

# USER AUTH VIEWS


class RegisterView(CreateView):
     form_class = UserRegForm
     template_name = 'shop/registration_form.html'

     # display the template when this view is called - when the user requests the page itself
     def get(self, request):
         #display the form - None ensures that there won't be any data in it.. yet
         form = self.form_class(None)
         return render(request, self.template_name, {'form': form})

     def post(self, request):
         form = self.form_class(request.POST)

         if form.is_valid():
             user = form.save(commit=False)

             username = form.cleaned_data['username']
             password = form.cleaned_data['password']

             user.set_password(password)
             user.save()

             user = authenticate(username=username, password=password)

             if user is not None:
                 if user.is_active:
                     login(request, user)
                     return HttpResponseRedirect('/shop/')
                 else:
                     return HttpResponseRedirect('/shop/')

         return render(request, self.template_name, {'form': form})


class LoginView(View):
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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/shop/')