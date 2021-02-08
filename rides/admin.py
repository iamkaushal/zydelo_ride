from django.contrib import admin
from .models import Ride, Request, Trip, Payment

# Registering models for admin dashboard
admin.site.register(Ride)
admin.site.register(Request)
admin.site.register(Trip)
admin.site.register(Payment)
