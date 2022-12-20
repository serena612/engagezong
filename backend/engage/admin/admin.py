from django.shortcuts import render
from django.contrib import admin
from django.urls import path

class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(r'cashdash/', self.admin_view(self.cash_dash_view)),
            path(r'datasync/', self.admin_view(self.datasync_dash_view)),
            path(r'prize/', self.admin_view(self.prize_dash_view)),
            path(r'subunsub/', self.admin_view(self.subunsub_dash_view)),
        ]
        urls = my_urls + urls
        return urls
    def cash_dash_view(self, request):
        return render(request, 'admin/iframes/cash.html')
    def datasync_dash_view(self, request):
        return render(request, 'admin/iframes/datasync.html')
    def prize_dash_view(self, request):
        return render(request, 'admin/iframes/prize.html')
    def subunsub_dash_view(self, request):
        return render(request, 'admin/iframes/subunsub.html')