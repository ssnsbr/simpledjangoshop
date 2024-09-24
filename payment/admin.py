from django.contrib import admin

from .models import VendorPayment,UserPayment

admin.site.register(VendorPayment)
admin.site.register(UserPayment)
