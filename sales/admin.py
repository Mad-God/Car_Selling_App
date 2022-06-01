from django.contrib import admin
from .models import CarCompany, SellCarListing, CarSaleRecord

# Register your models here.

admin.site.register(CarCompany)
admin.site.register(SellCarListing)
admin.site.register(CarSaleRecord)