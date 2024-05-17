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