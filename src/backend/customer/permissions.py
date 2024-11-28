from ..base.api.permissions import (AllowAny, IsAuthenticated, ResourcePermission, IsSuperUser, IsTheSameUser,
                                    CustomerPerm, AllOnlyGetPerm)


class CustomerPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = None
    global_perms = None
    retrieve_perms = IsAuthenticated()
    create_perms = IsAuthenticated()
    update_perms = IsTheSameUser()
    partial_update_perms = IsTheSameUser()
    destroy_perms = IsSuperUser() | IsTheSameUser()
    list_perms = IsAuthenticated()
    customer_user_perms = IsTheSameUser() | AllOnlyGetPerm()
    grievance_perms = CustomerPerm()
