from django.contrib.admin import apps

class MyAdminConfig(apps.AdminConfig):
    default_site = 'engage.admin.admin.MyAdminSite'
    # label = 'admin'
    # name = 'engage.admin'
    # def ready(self):
        # from django.contrib import admin
        # from django.contrib.contenttypes.models import ContentType
        # from django.contrib.admin.models import LogEntry, ADDITION
        