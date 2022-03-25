import imp
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import NewUserForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class LoginView(TemplateView):
    template_name = "login/login.html"

    def get(self, request):
        form = LoginForm()
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST or None)
        #import pdb; pdb.set_trace()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
              #  attempt = request.session.get("attempt")
             #   request.session['attempt'] += 1
                return redirect("blogs:index")
            else:
                messages.error(request, "Invalid username or password.")
         
        return render(request, self.template_name, {"form": form, "invalid_user": True})
                

class RegisterView(TemplateView):
    template_name = "login/registration.html"  

    def get(self, request):
        form = NewUserForm()
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = NewUserForm(request.POST)

        if form.is_valid():
            
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            raw_password = form.cleaned_data.get('password1')
            username = form.cleaned_data.get('username')
            form.save()
            
            return redirect('users:login')
        else:
            return render(request, self.template_name, {'form': form, 'invalid': 'Please try again.'})

def log_out(request):
    logout(request)
    return redirect("users:login")

    