from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, OrderForm
from .models import InventoryItem, Author, Order
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages

#basic homepage with text
class Index(TemplateView):
	template_name = 'inventory/index.html'

class Dashboard(LoginRequiredMixin, View): #LoginRequiredMixin makes dashboard inaccessible unless logged in
	def get(self, request):
		item = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')
		
		low_inventory = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		)

		if low_inventory.count() > 0:
			if low_inventory.count() > 1:
				#show message
				messages.error(request, f'{low_inventory.count()} items have low inventory')
			else:
				#message
				messages.error(request, f'{low_inventory.count()} item has low inventory')

		low_inventory_ids = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

		return render(request, 'inventory/dashboard.html', {'item' : item, 'low_inventory_ids': low_inventory_ids})

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/emp_signup.html', {'form': form}) #returns empty form

	def post(self, request):
		form = UserRegisterForm(request.POST) #gets submitted data

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			) # checks if form is valid, then saves it and logs user in

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/emp_signup.html', {'form': form}) #if not valid this redirects to original page

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard') #redirects to dashboard if successful

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['authors'] = Author.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'

class OrderList(LoginRequiredMixin, View):
	def get(self, request):
		orders = Order.objects.all()
		return render(request, 'inventory/order_list.html', {'orders': orders})

class CreateOrder(LoginRequiredMixin, View):
	def get(self, request):
		form = OrderForm()
		return render(request, 'inventory/create_order.html', {'form': form})

	def post(self, request):
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('order_list')
		return render(request, 'inventory/create_order.html', {'form': form})

def update_item_quantity(request, item_id, new_quantity):
	item = get_object_or_404(InventoryItem, id = item_id)
	item.quantity = new_quantity
	item.reordered = False # Reset the flag
	item.save()
	return redirected('dashboard')

def bookList(request):
	book = InventoryItem.objects.all()
	return render(request, 'inventory/book_list.html', {'book': book})

def book_detail(request, isbn):
	book = InventoryItem.objects.get(ISBN=isbn)
	return render(request, 'inventory/book_detail.html', {'book': book})