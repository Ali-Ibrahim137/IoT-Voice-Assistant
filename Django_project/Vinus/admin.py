from django.contrib import admin
from .models import Device, THINGER_API, Resources

admin.site.register(Device)
admin.site.register(THINGER_API)
admin.site.register(Resources)
