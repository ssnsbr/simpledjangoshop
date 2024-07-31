from django.contrib import admin

# Register your models here.

from .models import Vendor,VendorProduct

admin.site.register(Vendor)
admin.site.register(VendorProduct)