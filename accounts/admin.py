from django.contrib import admin
from .models import Profile

# registering Profile model for admin dashboard
admin.site.register(Profile)
