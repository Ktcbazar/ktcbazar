from django.contrib import admin
from .models import CustomUser, StaffProfile, Product


admin.site.register(CustomUser)
admin.site.register(StaffProfile)
admin.site.register(Product)