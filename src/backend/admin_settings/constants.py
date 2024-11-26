ROLES_PERMISSIONS = []
CONFIG = []
NON_CORE_SERVICES = "Non Core Services"
CORE_SERVICES = "Core Services"
PROFESSION = "Profession"
SETTINGS_CONSTANT = [
    {'title': 'Gender', 'can_disabled': False, 'children': []},
    {'title': PROFESSION, 'can_disabled': False, 'children': []},
    {'title': CORE_SERVICES, 'can_disabled': True, 'children': []},
    {'title': NON_CORE_SERVICES, 'can_disabled': True, 'children': []},
    {'title': 'Policies', 'can_disabled': False, 'children': []},
    {'title': 'Employee Policies', 'can_disabled': False, 'children': []},
]

# Log Actions

ACTION_OBJECT = {
    'Location': 'location',
    'DynamicSettings': 'dynamic setting'
}

# Log Category and sub category
# Categories
SETTINGS = "Settings"
PASSWORD = "password"

# Sub categories
HR_SETTINGS = "Admin settings"
RESET_PASSWORD = "Reset Password"

CA = "CA"
ADVOCATE = "Advocate"
CS = "CS"
CMA = "CMA"
ACCOUNTANT = "Accountant"
OTHER = "Other"

PROFESSIONS = ((CA, CA), (ADVOCATE, ADVOCATE), (CS, CS), (CMA, CMA),
               (ACCOUNTANT, ACCOUNTANT), (OTHER, OTHER))

LEAD = "Lead"

ACTIVE = "Active"
DEACTIVE = "Deactive"
ABSCOND = "Abscond"
RETIRED = "Retired"
LEAVED = "Leaved"

employee_STATUS = ((ACTIVE, ACTIVE), (DEACTIVE, DEACTIVE),
                  (ABSCOND, ABSCOND), (RETIRED, RETIRED),
                  (LEAVED, ACTIVE))

BLOOD_GROUPS = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)
