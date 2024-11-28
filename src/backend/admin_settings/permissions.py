from ..base.api.permissions import (AllowAny, IsAuthenticated, PermissionComponent, ResourcePermission, IsSuperUser,
                                    AllOnlyGetPerm, AllowAnyGetPerm, HRPerm, EmployeePerm, EmployeePermOnlyGet)


class DynamicSettingsPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = None
    global_perms = None
    retrieve_perms = IsSuperUser() | IsAuthenticated() | HRPerm()
    create_perms = IsSuperUser() | HRPerm()
    update_perms = IsSuperUser() | HRPerm()
    partial_update_perms = IsSuperUser() | HRPerm()
    destroy_perms = IsSuperUser() | HRPerm()
    list_perms = IsSuperUser() | IsAuthenticated() | AllOnlyGetPerm() | HRPerm()
    dropdown_perms = IsSuperUser() | AllOnlyGetPerm() | HRPerm()
    users_perms = IsSuperUser() | HRPerm()
    country_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    state_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    city_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    employee_perms = IsSuperUser() | HRPerm() | EmployeePermOnlyGet()
    deleted_employee_perms = IsSuperUser() | HRPerm() | EmployeePerm()
    role_perms = EmployeePerm() | HRPerm()
