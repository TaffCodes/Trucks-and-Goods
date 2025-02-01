# core/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group

class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group_name = form.cleaned_data.get('group')
        if group_name:
            group = Group.objects.get(name=group_name)
            obj.groups.add(group)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)