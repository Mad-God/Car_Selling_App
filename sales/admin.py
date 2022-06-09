from django.contrib import admin
from .models import CarInfo, CarSaleRecord, User

# Register your models here.

admin.site.register(CarInfo)
admin.site.register(User)
admin.site.register(CarSaleRecord)
