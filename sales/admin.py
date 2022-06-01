from django.contrib import admin
from .models import Company, Listing, Sale

# Register your models here.

admin.site.register(Company)
admin.site.register(Listing)
admin.site.register(Sale)