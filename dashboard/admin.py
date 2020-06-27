from django.contrib import admin

# Register your models here.
from .models import Room, Control, Sensor

admin.site.register(Room)
admin.site.register(Control)
admin.site.register(Sensor)
