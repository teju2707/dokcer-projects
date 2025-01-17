from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from models import db, User  # Import db and User model from models.py
from config import SECRET_KEY  # Import the secret key from config.py

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/flaskdb'  # Update with correct credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db.init_app(app)  # Initialize the database with the Flask app

# User registration route
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()  # Get the data sent in the request
    hashed_password = generate_password_hash(data['password'], method='sha256')  # Hash the password
    new_user = User(username=data['username'], password=hashed_password)  # Create a new user
    db.session.add(new_user)  # Add the user to the session
    db.session.commit()  # Commit the changes to the database
    return jsonify({'message': 'User registered successfully'}), 201  # Return a success message

# User login route
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()  # Get the login credentials from the request
    user = User.query.filter_by(username=data['username']).first()  # Search for the user in the database
    if not user or not check_password_hash(user.password, data['password']):  # Check if credentials are correct
        return jsonify({'message': 'Invalid credentials'}), 401  # Return error if invalid
    
    # Generate JWT token with expiration time (1 hour)
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})  # Return the generated token

# Protected route to demonstrate JWT authentication
@app.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization').split(" ")[1]  # Get token from the Authorization header
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # Decode the JWT token
        user = User.query.get(decoded_token['user_id'])  # Retrieve the user from the database
        return jsonify({'username': user.username}), 200  # Return user details
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401  # Handle token expiration
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401  # Handle invalid token

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app on all IP addresses on port 5000
