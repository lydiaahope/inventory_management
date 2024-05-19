from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
	name = models.CharField(max_length=200)
	quantity = models.IntegerField()
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, blank=True, null=True)
	ISBN = models.CharField(max_length=200, default='')
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE) #if user deleted, all their invtoryitems are deleted
	threshold = models.IntegerField(default=1)
	reordered = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Author(models.Model):
	name = models.CharField(max_length=200)

	class Meta: 
		verbose_name_plural = 'authors'

	def __str__(self):
		return self.name
		
class Order(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return f"Order for {self.item.name} on {self.order_date}"

class Sale(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=
		'01')
	customer_name = models.CharField(max_length=100, default='Unknown Customer')
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Sale by {self.user.username} to {self.customer_name} on {self.date.strftime('%Y-%m-%d')}"

class SaleItem(models.Model):
	sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
	item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.quantity} of {self.item.name} at {self.price} each"



