from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetCode


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_active',)
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (('Permissions'), {'fields': ('is_active','is_superuser', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    pass
