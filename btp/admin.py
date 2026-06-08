from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User, Group

admin.site.site_header = "Administration BTP"
admin.site.site_title = "Admin BTP"
admin.site.index_title = "Gestion du système BTP"