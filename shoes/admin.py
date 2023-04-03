from django.contrib import admin
from .models import *
from .form import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


admin.site.register(Shoe)
admin.site.register(User_Order)
admin.site.register(Order)
