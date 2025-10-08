from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transactions
from django import forms

class Register(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transactions
        fields=['amount','type','category','date','notes']