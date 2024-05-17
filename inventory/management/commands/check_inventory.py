from django.core.management.base import BaseCommand
from inventory.models import InventoryItem, Order

class Command(BaseCommand):
    help = 'Check inventory levels and generate orders if necessary'

    def handle(self, *args, **kwargs):
        items = InventoryItem.objects.all()
        for item in items:
            if item.quantity <= item.threshold:
                order = Order.objects.create(item=item, quantity=item.threshold - item.quantity + 1, manufacturer='Default Manufacturer')
                self.stdout.write(self.style.SUCCESS(f'Order created for {item.name}'))

# def handle(self, *args, **kwargs):
        #low_inventory_items = InventoryItem.objects.filter(quantity__lte=F('threshold'))
        #for item in low_inventory_items:
           # Order.objects.create(
                #item=item,
               # quantity=item.threshold - item.quantity,
               # manufacturer='Default Manufacturer'
          #  )
            #self.stdout.write(f'Order created for {item.name}')