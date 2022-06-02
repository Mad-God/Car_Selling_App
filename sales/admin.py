from django.contrib import admin
from .models import SellCarListing, CarSaleRecord

# Register your models here.

admin.site.register(SellCarListing)
admin.site.register(CarSaleRecord)