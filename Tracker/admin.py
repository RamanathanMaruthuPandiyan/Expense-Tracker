from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Expenses)
admin.site.register(Session)