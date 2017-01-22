from .forms import UserLogForm, UserRegForm
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect

# USER AUTH VIEWS

# registration view - allows for the user to register
class RegisterView(CreateView):
     form_class = UserRegForm
     template_name = 'shop/registration_form.html'

     # display the template when this view is called - when the user requests the page itself
     def get(self, request):
         #display the form - None ensures that there won't be any data in it upon the user first accessing page
         form = self.form_class(None)
         return render(request, self.template_name, {'form': form})

    # when a post request) form submission is passed then do the following
     def post(self, request):
         form = self.form_class(request.POST)

         if form.is_valid():
             user = form.save(commit=False)

             username = form.cleaned_data['username']
             password = form.cleaned_data['password']

            # set_password encrypots the password (NO PLAIN_TEXT PASSWORDS)
             user.set_password(password)
             # write user to database
             user.save()

             # once user is saved, authenticate (log them in ) by getting the username and password
             user = authenticate(username=username, password=password)

             # if there is indeed a user saved and present with those details and then log them in if they're an active user - then redirect to the shop homepage
             if user is not None:
                 if user.is_active:
                     login(request, user)
                     return HttpResponseRedirect('/shop/')
                 else:
                     return HttpResponseRedirect('/shop/')
         # if something went wrong, re-render the register page with that form alogn with the data that was sent.
         return render(request, self.template_name, {'form': form})


# Login view to allow user to login
class LoginView(View):
    form_class = UserLogForm
    template_name = 'shop/login.html'

    # the request that will render the form.
    def get(self, request):
        form = self.form_class(None)
        # render the form in the template.
        return render(request, self.template_name, {'form': form})

    # This handles login submission
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # authenticate the user with 
        user = authenticate(username=username, password=password)

        # if the user exists and their status is active on the db then log them in
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/shop/')
            else:
                return HttpResponseRedirect('/shop/login')
        return HttpResponseRedirect('/shop/login')

# allows for the logging out of the user
class LogoutView(View):
    def get(self, request):
        logout(request)
        # send them back to the homepage
        return HttpResponseRedirect('/shop/')
