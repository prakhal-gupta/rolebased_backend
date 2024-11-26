from ..base.api.permissions import (AllowAny, PermissionComponent, ResourcePermission, IsSuperUser)


class IsTheSameUser(PermissionComponent):
    def has_permission(self, request, view):
        if not request.user.pk:
            return False
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj=None):
        if not request.user.pk:
            return False
        return request.user.is_authenticated() and request.user.pk == obj.pk


class UserPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = None
    global_perms = None
    retrieve_perms = IsTheSameUser()
    create_perms = None
    update_perms = IsTheSameUser()
    partial_update_perms = IsTheSameUser()
    destroy_perms = IsTheSameUser()
    login_perms = AllowAny()
    employee_login_perms = AllowAny()
    customer_login_perms = AllowAny()
    superuser_login_perms = IsSuperUser()
    user_clone_perms = AllowAny()
    customer_clone_perms = AllowAny()
    password_change_perms = AllowAny()
    register_perms = AllowAny()
    user_reset_mail_perms = AllowAny()
    reset_password_perms = AllowAny()
    admin_list_perms = AllowAny()
    customer_register_perms = AllowAny()
