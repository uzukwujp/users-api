from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from werkzeug.utils import secure_filename
from services.user_service import UserService
from config import ALLOWED_EXTENSIONS

user_bp = Blueprint('users', __name__)
user_service = UserService()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Endpoint to get all users."""
    try:
        users = user_service.get_all_users()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint to create a new user with optional avatar."""
    try:
        # Handle form data (including JSON fallback)
        if request.is_json:
            data = request.get_json()
            avatar_file = None
        else:
            data = request.form.to_dict()
            avatar_file = request.files.get('avatar')
            
            if avatar_file and not allowed_file(avatar_file.filename):
                return jsonify({"error": "File type not allowed"}), 400

        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Create user with optional avatar
        user = user_service.create_user(data, avatar_file)
        return jsonify(user.to_dict()), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500