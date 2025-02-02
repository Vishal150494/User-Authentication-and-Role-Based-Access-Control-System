"""
Role-based Access control

This module provides functionality for role-based access control (RBAC) in a system.

Classes:
    User: Represents a user in the system.
    Role: Represents a role that can be assigned to users.
    Permission: Represents a permission that can be assigned to roles.
    AccessControl: Manages the assignment of roles and permissions to users.

Functions:
    add_user(username): Adds a new user to the system.
    add_role(role_name): Adds a new role to the system.
    add_permission(permission_name): Adds a new permission to the system.
    assign_role_to_user(username, role_name): Assigns a role to a user.
    assign_permission_to_role(role_name, permission_name): Assigns a permission to a role.
    check_user_permission(username, permission_name): Checks if a user has a specific permission.
"""