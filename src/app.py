
from flask import Flask
from flask_cors import CORS
from controllers.user_controller import user_bp
from config import DEBUG, HOST, PORT

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)