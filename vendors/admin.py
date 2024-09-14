from django.contrib import admin

# Register your models here.

from .models import Vendor, VendorProduct, VendorTransaction

admin.site.register(Vendor)
admin.site.register(VendorProduct)
admin.site.register(VendorTransaction)
