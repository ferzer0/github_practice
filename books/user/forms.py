from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("email")
        uname = User.objects.get(Username__iexact=username)
        if not uname.exists():
            raise forms.ValidationError("Invalid User.")
        return       


class NewUserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='', widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=30, help_text='', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = "confirmation password"
        self.fields['password1'].label = "password"

    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]
    


class SettingForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=100, help_text='', widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

    def clean_email(self):
        if self.instance: 
            return self.instance.email
        else: 
            return self.fields['email']