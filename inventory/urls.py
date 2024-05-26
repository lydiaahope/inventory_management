from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, OrderListView, CreateOrder, SaleCreateView, SaleItemCreateView, SaleListView, SaleDetailView, ReportView, export_sales, export_inventory, CartView, AddToCartView, CartItemDeleteView, OrderDetailView, OrderUpdateView, OrderStatusUpdateView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', Index.as_view(), name = 'index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'), #<int:pk> lets it know we need an int as primarykey
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('orders/', OrderListView.as_view(), name = 'order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('orders/create/', CreateOrder.as_view(), name = 'create_order'),
    path('emp_signup/', SignUpView.as_view(), name='emp_signup'),
    path('emp_login/', auth_views.LoginView.as_view(template_name='inventory/emp_login.html'), name='emp_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('books', views.bookList, name='book_list'),
    path('books/<str:isbn>', views.book_detail, name='book_detail'),
    path('sale/add/', SaleCreateView.as_view(), name = 'sale_add'),
    path('sale/<int:sale_id>/add-item/', SaleItemCreateView.as_view(), name = 'sale_item_add'),
    path('sales/', SaleListView.as_view(), name = 'sale_list'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name = 'sale_detail'),
    path('reports/', ReportView.as_view(), name = 'report'),
    path('export_sales/', export_sales, name = 'export_sales'),
    path('export_inventory/', export_inventory, name = 'export_inventory'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:item_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/delete/<int:item_id>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
    path('contact_us', views.contact_us, name='Contact_us')
]
# path('') points rootpath to Index.as_view() and loads index page
