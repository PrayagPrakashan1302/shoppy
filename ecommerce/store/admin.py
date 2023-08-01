
from django.contrib import admin
from .models import Product, Customer, Order, OrderItem, ShippingAddress,OrderDetails

# Register your models here.

admin.site.register(Product)

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(OrderDetails)

