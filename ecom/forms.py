from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.forms import ModelForm


class SignUp(UserCreationForm):
    name = forms.CharField(max_length=40)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.IntegerField()
    address = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["name",'username','password1','password2','phone','email','address']
