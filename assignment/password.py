class Password:  # Changed to PascalCase for class naming convention
    def __init__(self):
        pass  # No need to initialize attributes since they're not used
    
    @staticmethod  # Changed to static methods since we don't use instance attributes
    def check_password(password):
        """
        Validates password requirements.
        Password must be at least 8 characters long and contain letters and numbers.
        Raises ValueError if requirements not met.
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number")
        if not any(char.isalpha() for char in password):
            raise ValueError("Password must contain at least one letter")
        return True

    def check_username(username):
        """
        Validates username requirements.
        Username must be at least 5 characters long and alphanumeric.
        Raises ValueError if requirements not met.
        """
        if len(username) < 5:
            raise ValueError("Username must be at least 5 characters long")
        if not username.isalnum():
            raise ValueError("Username must contain only letters and numbers")
        return True