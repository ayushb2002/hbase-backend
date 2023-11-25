from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from utils.auth_utils import AuthUtils

app = Flask(__name__)
api = Api(app)

hbase_host = 'hadoop'  
hbase_port = 9090 
auth_utils = AuthUtils(hbase_host, hbase_port)

# Initialize HBase table for users if it doesn't exist
if b'users' not in auth_utils.connection.tables():
    auth_utils.create_user_table()

# API resource for user registration
class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            response = {'error': 'Username and password are required'}
            return jsonify(response)

        try:
            auth_utils.add_user(username, password)
            response = {'message': 'User registered successfully'}
            return jsonify(response)
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response)

# API resource for user authentication
class Authenticate(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            response = {'error': 'Username and password are required'}
            return jsonify(response)

        try:
            user_data = auth_utils.get_user(username)
            if user_data and user_data['auth:password'] == password:
                response = {'message': 'Authentication successful'}
                return jsonify(response)
            else:
                response = {'error': 'Authentication failed'}
                return jsonify(response)
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response)

api.add_resource(Register, '/register')
api.add_resource(Authenticate, '/authenticate')

if __name__ == '__main__':
    app.run(debug=True)