from ..base.api.permissions import (AllowAny, IsAuthenticated, ResourcePermission, IsSuperUser, AllOnlyGetPerm,
                                    IsTheSameUser, ApprovalPerm, HRPerm)

class EmployeePermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = None
    global_perms = None
    retrieve_perms = IsSuperUser() | IsAuthenticated()
    create_perms = IsSuperUser()
    update_perms = IsSuperUser() | IsTheSameUser()
    partial_update_perms = IsSuperUser() | IsTheSameUser()
    destroy_perms = IsSuperUser()
    list_perms = IsSuperUser() | IsAuthenticated() | AllOnlyGetPerm()
    hod_approval_perms = ApprovalPerm()
    hr_approval_perms = HRPerm()
