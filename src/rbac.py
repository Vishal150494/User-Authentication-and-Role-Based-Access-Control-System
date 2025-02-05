"""
Role-based Access control

This module provides functionality for role-based access control (RBAC) in a system.

Classes:
    User: Represents a user in the system.
    Role: Represents a role that can be assigned to users.
    Permission: Represents a permission that can be assigned to roles.
    AccessControl: Manages the assignment of roles and permissions to users.

Functions:
    add_role(role_name): Adds a new role to the system.
    remove_role(role_name): Removes a role from the system
    add_permission(permission_name): Adds a new permission to the system.
    remove_permission(permission_name): Removes a permission from the system
    assign_role_to_user(username, role_name): Assigns a role to a user.
    remove_role_from_user(username, role_name): Removes a role assigned to a user
    assign_permission_to_role(role_name, permission_name): Assigns a permission to a role.
    check_user_permission(username, permission_name): Checks if a user has a specific permission.
"""
import json

RBAC_FILE= 'data/rbac_data.json'
class RBACManager:
    def __init__(self):
        self.data = self._load_rbac_data()
        
    def _load_rbac_data(self):
        """Load the rbac_data.json file

        Returns:
            dict: JSON file content if present, empty dict otherwise
        """
        try:
            with open(RBAC_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": {}, "roles": {}, "permissions": {}}
        
    def _save_rbac_data(self):
        """Saves RBAC data to the rbac_data.json

        Returns:
            dict: roles nad permissions associated with eacch user
        """
        with open(RBAC_FILE, 'w') as file:
            return json.dump(self.data, file, indent=4)
        
    def add_role(self, role: str):
        """Add a new role to the system

        Args:
            role (str): user role

        Returns:
            bool: True if role added successfully, False otherwise
        """
        if role in self.data['roles']:
            print(f"Role '{role}' already exists.")
            return False
        
        self.data['roles'][role] = []
        self._save_rbac_data()
        print(f"Role '{role}' added successfully.")
        return True
    
    def remove_role(self, role: str):
        """Remove a role from the system

        Args:
            role (str): user role

        Returns:
            bool: True if role removed successfully, False otherwise
        """
        if role not in self.data["roles"]:
            print(f"Role '{role}' not found in the system.")
            return False
        
        del self.data["roles"][role]
        self._save_rbac_data()
        print(f"Role '{role}' removed successfully.")
        return True
    
    def add_permission(self, permission_name: str):
        """Add a new permission to the system

        Args:
            permission_name (str): name of the permission
        
        Returns:
            bool: True if permission added successfully, False otherwise
        """
        if permission_name in self.data["permissions"]:
            print(f"Permission '{permission_name}' already exists.")
            return False
        
        self.data["permissions"][permission_name] = []
        self._save_rbac_data()
        print(f"Permission '{permission_name}' added successfully.")
        return True
    
    def remove_permission(self, permission_name: str):
        """Remove a permission from the system

        Args:
            permission_name (str): name of the permission
            
        Returns:
            bool: True if permission removed successfully, False otherwise
        """
        if permission_name not in self.data["permissions"]:
            print(f"Permission '{permission_name}' does not exist.")
            return False
        
        del self.data["permissions"][permission_name]
        self._save_rbac_data()
        print(f"Permission '{permission_name}' removed successfully.")
        return True
    
    def assign_role_to_user(self, username: str, role: str):
        """Assign a specific role to a user

        Args:
            username (str): username
            role (str): role

        Returns:
            bool: True if role is successful assigned to user, False otherwise
        """
        if username not in self.data["users"]:
            self.data["users"][username] = []
            
        if role not in self.data["roles"]:
            print(f"Role '{role}' does not exist.")
            return False
        
        if role in self.data["users"][username]:
            print(f"User '{username}' already has role '{role}'.")
            return False
        self.data["users"][username].append(role)
        self._save_rbac_data()
        print(f"Role '{role}' has been assigned to user '{username}'.")
        return True
    
    def remove_role_from_user(self, username: str, role: str):
        """Remove a role from a user

        Args:
            username (str): username
            role (str): role name

        Returns:
            bool: True if role removed from a user, False otherwise
        """
        if username not in self.data["users"]:
            print(f"User '{username}' does not exist.")
            return False
        
        if role not in self.data["roles"]:
            print(f"Role '{role}' does not exist.")
            return False
        
        if role not in self.data["users"][username]:
            print(f"User '{username}' does not have role '{role}'.")
            return False
        
        self.data["users"][username].remove(role)
        self._save_rbac_data()
        print(f"Role '{role}' removed from user '{username}'.")
        return True
    
    def assign_permission_to_role(self, role: str, permission_name: str):
        """Assign permission to specific role

        Args:
            role (str): role name
            permission_name (str): permission name

        Returns:
            bool: True if permission assigned to role, False other wise
        """
        if permission_name not in self.data["permissions"]:
            print(f"Permission '{permission_name}' does not exist.")
            return False
        
        if role not in self.data["roles"]:
            print(f"Role '{role}' does not exist.")
            return False
        
        if permission_name in self.data["roles"][role]:
            print(f"Role '{role}' already has permission '{permission_name}'.")
            return False
        
        self.data["roles"][role].append(permission_name)
        self._save_rbac_data()
        print(f"Permission '{permission_name}' assigned to role '{role}'.")
        return True
    
    def check_user_permission(self, username: str, permission_name: str):
        """Check permission for specific user

        Args:
            username (str): username
            permission_name (str): permission name

        Returns:
            bool: True if username found in the system, False otherwise
        """
        if username not in self.data["users"]:
            print(f"User '{username}' not found.")
            return False
        
        user_data = self.data["users"][username]
        # Check user specific permission first
        if permission_name in user_data.get("permissions", []):
            print(f"User '{username}' has permission '{permission_name}' (user-specific).")
            return True

        # Check role based permissions
        for role in user_data.get["roles", []]:
            if permission_name in self.data["roles"].get(role, {}):
                print(f"User '{username}' has permission '{permission_name}'.")
                return True
            
        print(f"User '{username}' does not have permission '{permission_name}'.")
        return False