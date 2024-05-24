from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Author, InventoryItem, Order, Sale, SaleItem, CartItem

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
		fields = ['name', 'quantity', 'author', 'ISBN', 'description']
		widgets = {
			'ISBN': forms.TextInput(attrs={'maxlength': 13, 'minlength': 13}),
		}
		error_messages = {
			'ISBN': {
				'unique': "An item with this ISBN already exists.",
				'min_length': "The ISBN must be exactly 13 characters long.",
			},
		}

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['item', 'quantity', 'manufacturer']

class SaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields = ['user', 'customer_name', 'total_amount']

class SaleItemForm(forms.ModelForm):
	class Meta:
		model = SaleItem
		fields = ['item', 'quantity', 'price']

class CartItemForm(forms.ModelForm):
	class Meta:
		model = CartItem
		fields = ['item', 'quantity'] #item same as where inventory item was referenced, can be changed

