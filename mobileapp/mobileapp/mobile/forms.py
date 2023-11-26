from django import forms
from mobile.models import Mobiles
from django.contrib.auth.models import User

class MobileForm(forms.ModelForm):
    class Meta:
        model=Mobiles
        fields="__all__"

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "brand":forms.TextInput(attrs={"class":"form-control"}),
            "specs":forms.TextInput(attrs={"class":"form-control"}),
            "display":forms.TextInput(attrs={"class":"form-control"}),
           
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()