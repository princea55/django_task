from django import forms
from .models import Restaurant
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CreateOwner(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class AddRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['ownerId','name', 'city', 'address', 'franchise_name']

class LoginUser(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
