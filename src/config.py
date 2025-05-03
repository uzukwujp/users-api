import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
# In Kubernetes, these will come from mounted secrets
load_dotenv()

# AWS Configuration
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
# No default values for credentials - will use IAM role when not specified
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'Users')
S3_BUCKET = os.environ.get('S3_BUCKET', 'prima-tech-challenge')
S3_AVATAR_PREFIX = os.environ.get('S3_AVATAR_PREFIX', 'avatars/')

# Flask Configuration
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size