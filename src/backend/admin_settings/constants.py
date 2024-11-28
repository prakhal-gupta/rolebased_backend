ROLES_PERMISSIONS = []
CONFIG = []
PROFESSION = "Profession"
SETTINGS_CONSTANT = [
    {'title': 'Gender', 'can_disabled': False, 'children': []},
    {'title': PROFESSION, 'can_disabled': False, 'children': []}
]

CA = "CA"
ADVOCATE = "Advocate"
CS = "CS"
CMA = "CMA"
ACCOUNTANT = "Accountant"
OTHER = "Other"
PROFESSIONS = ((CA, CA), (ADVOCATE, ADVOCATE), (CS, CS), (CMA, CMA),(ACCOUNTANT, ACCOUNTANT), (OTHER, OTHER))

ACTIVE = "Active"
DEACTIVE = "Deactive"
ABSCOND = "Abscond"
RETIRED = "Retired"
LEAVED = "Leaved"
employee_STATUS = ((ACTIVE, ACTIVE), (DEACTIVE, DEACTIVE),(ABSCOND, ABSCOND), (RETIRED, RETIRED),(LEAVED, ACTIVE))

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
