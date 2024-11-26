from ..base.api.permissions import (AllowAny, IsAuthenticated, PermissionComponent, ResourcePermission, IsSuperUser,
                                    AllOnlyGetPerm)


class IsTheSameUser(PermissionComponent):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj=None):
        return request.user.is_authenticated() and request.user.pk == obj.pk


class CustomerPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = None
    global_perms = None
    retrieve_perms = IsSuperUser() | IsAuthenticated()
    create_perms = IsSuperUser()
    update_perms = IsSuperUser()
    partial_update_perms = IsSuperUser()
    destroy_perms = IsSuperUser()
    list_perms = IsSuperUser() | IsAuthenticated() | AllOnlyGetPerm()
    customer_perms = IsAuthenticated()
    grievance_perms = IsAuthenticated()
