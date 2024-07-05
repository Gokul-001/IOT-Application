from django.contrib import admin
from .models import Device,TemperatureReadings,HumidityReadings
# Register your models here.

admin.site.register(Device)
admin.site.register(TemperatureReadings)
admin.site.register(HumidityReadings)