from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import *

admin.site.register(User, UserAdmin)
admin.site.register(Category)

