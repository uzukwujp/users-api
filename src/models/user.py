
class User:
    """User model representing the user entity in the system."""
    
    def __init__(self, name, email, avatar_url=None):
        self.name = name
        self.email = email
        self.avatar_url = avatar_url

    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            "name": self.name,
            "email": self.email,
            "avatar_url": self.avatar_url
        }

    @classmethod
    def from_dict(cls, data):
        """Create User object from dictionary."""
        return cls(
            name=data.get('name'),
            email=data.get('email'),
            avatar_url=data.get('avatar_url')
        )