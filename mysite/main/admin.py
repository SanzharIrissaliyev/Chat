from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import *

class SiteuserAdmin(admin.ModelAdmin):
    pass
admin.site.register(Siteuser, SiteuserAdmin)



class SmsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sms, SmsAdmin)


class GroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(Group, GroupAdmin)
