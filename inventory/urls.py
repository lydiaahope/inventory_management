from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, OrderList, CreateOrder
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name = 'index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'), #<int:pk> lets it know we need an int as primarykey
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('orders/', OrderList.as_view(), name = 'order_list'),
    path('orders/create/', CreateOrder.as_view(), name = 'create_order'),
    path('emp_signup/', SignUpView.as_view(), name='emp_signup'),
    path('emp_login/', auth_views.LoginView.as_view(template_name='inventory/emp_login.html'), name='emp_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout')
]
# path('') points rootpath to Index.as_view() and loads index page