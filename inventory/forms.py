from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Author, InventoryItem, Order

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

#this is the form used to sign up users^^^

class InventoryItemForm(forms.ModelForm):
	author = forms.ModelChoiceField(queryset=Author.objects.all(), initial=0)
	class Meta:
		model = InventoryItem
		fields = ['name', 'quantity', 'author', 'ISBN']

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['item', 'quantity', 'manufacturer']

