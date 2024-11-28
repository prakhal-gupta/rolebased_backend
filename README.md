<b>Grievance Management(ROLE BASED Authentication)</b>

<b>Overview</b>

This is a Django-based backend project designed to manage a role-based grievance system. The project includes fundamental functionalities such as user authentication, role-based endpoint access, and a grievance approval workflow. Customers can submit grievances, which undergo a structured approval process by users with appropriate roles (Approval and HR).

<b>Features</b>

<b>Role-Based Authentication:</b>

Secure endpoints based on user roles (Customer, Approval, HR, etc.).
Integration with Django Rest Framework (DRF) for API security.

<b>User Management:</b>

Accounts app for managing user profiles and roles.

Token-based authentication using DRF.

<b>Grievance Management:</b>

Customers can submit grievances.
Approval and HR roles can review and approve grievances based on workflow rules.

<b>Modular Apps:</b>

<b>accounts:</b> User management and role-based authentication.

<b>admin_settings:</b> Application-wide settings managed by admins.

<b>employee:</b> Employee-specific operations.

<b>customer:</b> Customer-related operations, including grievance submission.

<b>Technologies Used</b>

<b>Framework:</b> Django, Django Rest Framework (DRF)

<b>Database:</b> PostgreSQL

<b>Authentication:</b> Role-based security using Django's built-in permissions and DRF token authentication.

<b>API Design:</b> RESTful APIs with DRF serializers and views.
