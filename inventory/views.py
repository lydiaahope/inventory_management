from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, OrderForm, SaleForm, SaleItemForm, CartItemForm
from .models import InventoryItem, Author, Order, Sale, SaleItem, Cart, CartItem  
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import HttpResponse
from django.db import models
import csv

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

class SaleCreateView(LoginRequiredMixin, CreateView):
	model = Sale 
	form_class = SaleForm 
	template_name = 'inventory/sale_form.html'
	success_url = reverse_lazy('dashboard')

	def form_valid(self, form):
		form.instance.user = self.request.user
		response = super().form_valid(form)
		#redirect to the sale item creation page
		return redirect('sale_item_add', sale_id=self.object.id)

	
class SaleItemCreateView(LoginRequiredMixin, CreateView):
	model = SaleItem 
	form_class = SaleItemForm
	template_name = 'inventory/sale_item_form.html'
	success_url = reverse_lazy('dashboard')

	def form_valid(self, form):
		form.instance.sale_id = self.kwargs['sale_id']
		return super().form_valid(form)


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'inventory/sale_list.html'
    context_object_name = 'sales'

class SaleDetailView(LoginRequiredMixin, ListView):
    model = SaleItem
    template_name = 'inventory/sale_detail.html'
    context_object_name = 'sale_items'

    def get_queryset(self):
        return SaleItem.objects.filter(sale_id=self.kwargs['pk'])

class ReportView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'inventory/report.html'
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sales data
        total_sales = Sale.objects.count()
        total_revenue = Sale.objects.aggregate(models.Sum('total_amount'))['total_amount__sum']
        context['total_sales'] = total_sales
        context['total_revenue'] = total_revenue
        
        # Inventory data
        total_items = InventoryItem.objects.count()
        low_inventory_items = InventoryItem.objects.filter(quantity__lte=1)  # Adjust threshold as needed
        context['total_items'] = total_items
        context['low_inventory_items'] = low_inventory_items

        # Add other necessary context data for reporting
        return context

def export_sales(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type = 'text/csv')
	response['Content-Disposition'] = 'attachment; filename="sales.csv"'

	writer = csv.writer(response)
	writer.writerow(['Customer Name', 'Total Amount', 'Date'])

	sales = Sale.objects.all().values_list('customer_name', 'total_amount', 'date')
	for sale in sales:
		writer.writerow(sale)

	return response

def export_inventory(request): #exports inventory data
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

	writer = csv.writer(response)
	writer.writerow(['Item Name', 'Quantity'])

	items = InventoryItem.objects.all().values_list('name', 'quantity')
	for item in items:
		writer.writerow(item)

	return response


class CartView(View):
	def get(self, request):
		if request.user.is_authenticated:
			cart, created = Cart.objects.get_or_create(user=request.user)
		else:
			cart = self.get_guest_cart(request)

		cart_items = CartItem.objects.filter(cart=cart)
		return render(request, 'inventory/cart.html', {'cart_items' : cart_items})

	def get_guest_cart(self, request):
		cart_id = request.session.get('guest_cart_id')
		if cart_id:
			cart = Cart.objects.filter(id=cart_id).first()
		else:
			cart = Cart.objects.create()
			request.session['guest_cart_id'] = cart.id
			return cart

class AddToCartView(View):
	def post(self, request, item_id):
		item = InventoryItem.objects.get(id=item_id)
		if request.user.is_authenticated:
			cart, created = Cart.objects.get_or_create(user=request.user)
		else:
			cart = self.get_guest_cart(request)

		CartItem.objects.create(cart=cart, item=item, quantity=1)
		return redirect('cart')

	def get_guest_cart(self, request):
		cart_id = request.session.get('guest_cart_id')
		if cart_id:
			cart = Cart.objects.filter(id=cart_id).first()
		else:
			cart = Cart.objects.create()
			request.session['guest_cart_id'] = cart.id
		return cart

class CartItemDeleteView(View):
	def post(self, request, item_id):
		if request.user.is_authenticated:
			cart = Cart.objects.get(user=request.user)
		else:
			cart = self.get_guest_cart(request)

		cart_item = CartItem.objects.get(cart=cart, item_id=item_id)
		cart_item.delete()
		return redirect('cart')

	def get_guest_cart(self, request):
		cart_id = request.session.get('guest_cart_id')
		if cart_id:
			cart = Cart.objects.filter(id=cart_id).first()
		else:
			cart = Cart.objects.create()
			request.session['guest_cart_id'] = cart.id
		return cart


