import boto3
import os
import uuid
from werkzeug.utils import secure_filename
from models.user import User
from config import (
    AWS_REGION, 
    AWS_ACCESS_KEY_ID, 
    AWS_SECRET_ACCESS_KEY, 
    DYNAMODB_TABLE, 
    S3_BUCKET, 
    S3_AVATAR_PREFIX,
    ALLOWED_EXTENSIONS
)

class UserService:
    """Service class to handle user business logic."""
    
    def __init__(self):
        # Initialize boto3 session
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID if AWS_ACCESS_KEY_ID else None,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY if AWS_SECRET_ACCESS_KEY else None,
            region_name=AWS_REGION
        )
        
        self.dynamodb = session.resource('dynamodb')
        self.s3 = session.client('s3')
        self.user_table = self.dynamodb.Table(DYNAMODB_TABLE)
        self.s3_bucket = S3_BUCKET
        self.avatar_prefix = S3_AVATAR_PREFIX

    def get_all_users(self):
        """Get all users from DynamoDB."""
        try:
            response = self.user_table.scan()
            return [User.from_dict(item) for item in response.get('Items', [])]
        except Exception as e:
            print(f"Error fetching users: {e}")
            raise

    def create_user(self, user_data, avatar_file=None):
        """
        Create a new user with optional avatar upload.
        
        Args:
            user_data: Dictionary containing user attributes
            avatar_file: Optional file object for avatar upload
            
        Returns:
            User: The created user object
        """
        try:
            # Process avatar upload if provided
            avatar_url = None
            if avatar_file:
                avatar_url = self._upload_avatar(avatar_file)

            # Create and save user
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                avatar_url=avatar_url
            )
            
            self.user_table.put_item(Item=user.to_dict())
            return user
            
        except Exception as e:
            print(f"Error creating user: {e}")
            raise

    def _upload_avatar(self, image_file):
        """Upload avatar to S3 and return URL (works with both secret keys & IAM roles)"""
        try:
            # Generate unique filename
            file_ext = os.path.splitext(image_file.filename)[1].lower()
            filename = f"{uuid.uuid4()}{file_ext}"
            s3_key = f"{self.avatar_prefix}{secure_filename(filename)}"
            
            # Upload configuration (ACL-free)
            extra_args = {
                'ContentType': image_file.content_type,
                # Removed ACL to comply with modern S3 security
            }

            # Upload to S3
            self.s3.upload_fileobj(
                image_file,
                self.s3_bucket,
                s3_key,
                ExtraArgs=extra_args
            )
            
            # Generate public URL (requires proper bucket policy)
            return f"https://{self.s3_bucket}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
            
        except Exception as e:
            print(f"Error uploading avatar: {e}")
            raise