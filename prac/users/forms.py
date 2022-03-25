from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

 #   def clean(self):
 #       email = self.cleaned_data.get("email")
 #       password = self.cleaned_data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("email")
        uname = User.objects.get(Username__iexact=username)
        if not uname.exists():
            raise forms.ValidationError("Invalid User.")
        return


class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='')
    first_name = forms.CharField(max_length=30, required=False, help_text='')
    last_name = forms.CharField(max_length=30, required=False, help_text='')
    username = forms.CharField(max_length=30, help_text='')
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = "%s.%s" %(self.cleaned_data['first_name'], self.cleaned_data['last_name'])
        if commit:
            user.save()
        return user