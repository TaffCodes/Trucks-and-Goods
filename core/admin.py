from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    add_form = UserCreationForm
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new user
            obj.set_password(form.cleaned_data.get('password1'))
            obj.is_active = True
            
        super().save_model(request, obj, form, change)
        
        # Handle group assignment
        group_name = form.cleaned_data.get('group')
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                obj.groups.add(group)
            except Group.DoesNotExist:
                pass

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)