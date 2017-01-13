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
    # form class for validation - matching passwords, etc etc
     form_class = UserRegForm
    # template to display
     template_name = 'shop/registration_form.html'

     # display the template when this view is called - when the user requests the page itself
     def get(self, request):
         #display the form - None ensures that there won't be any data in it.. yet
         form = self.form_class(None)
         return render(request, self.template_name, {'form': form})

    # when a post request) form submission is passed then do the following
     def post(self, request):
         form = self.form_class(request.POST)

        # if the form is valid
         if form.is_valid():
             # save form data
             user = form.save(commit=False)

            # get the username and wrap it in a variable
             username = form.cleaned_data['username']
             #get the password and wrap into a variable
             password = form.cleaned_data['password']

            # set_password to run the fucntion that encrypots the password (NO PLAIN_TEXT PASSWORDS)
             user.set_password(password)
             # save user to database
             user.save()

             # once user is saved, authenticate (log them in ) by getting the username and password
             user = authenticate(username=username, password=password)

             # if there is indeed a user saved and present qwith those details
             if user is not None:
                 # and if the user status is_active is set to "TRUE"
                 if user.is_active:
                     # log them in
                     login(request, user)
                     #send to the shop homepage
                     return HttpResponseRedirect('/shop/')
                 else:
                     #if not, send to homepage but don't log them in
                     return HttpResponseRedirect('/shop/')
         # if something went wrong, re-render the rewgister page with that form alogn with the data that was sent.
         return render(request, self.template_name, {'form': form})


# Login view to allow user to login
class LoginView(View):
    # form class in forms.py for login validation
    form_class = UserLogForm
    #template to render the form
    template_name = 'shop/login.html'

    # the request that will render the form.
    def get(self, request):
        # display the form with NO data as no POST request has been sent as of yet
        form = self.form_class(None)
        # render the form in the template.
        return render(request, self.template_name, {'form': form})

    # if POST data has been sent (login submission)
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
        # or else, just redirect tot he login page
        return HttpResponseRedirect('/shop/login')

# allows for the logging out of the user
class LogoutView(View):
    # this is a get request as no data is being sent.
    def get(self, request):
        # logout the current authenticated user
        logout(request)
        # send them back to the homepage
        return HttpResponseRedirect('/shop/')