from django.contrib import admin

# Register your models here.
from .models import VendorPayment,UserPayment

admin.site.register(VendorPayment)
admin.site.register(UserPayment)
