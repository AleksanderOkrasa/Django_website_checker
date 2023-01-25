from django.contrib import admin
from .models import UserData, WebpageData

#Register your models here.
# admin.site.register(User)
admin.site.register(UserData)
admin.site.register(WebpageData)

#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(Url)
# class UrlAdmin(admin.ModelAdmin):
#     pass