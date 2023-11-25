from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from utils.auth_utils import AuthUtils

app = Flask(__name__)
api = Api(app)

hbase_host = 'hadoop'  
hbase_port = 9090 
auth_utils = AuthUtils(hbase_host, hbase_port)

if b'users' not in auth_utils.connection.tables():
    auth_utils.create_user_table()

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

class UpdatePersonalInfo(Resource):
    def post(self, username):
        data = request.get_json()
        info = {
            'name': data.get('name'),
            'gender': data.get('gender'),
            'phone_number': data.get('phone_number'),
            'address': data.get('address'),
            'age': data.get('age'),
            'email': data.get('email'),
        }

        if any(value is None for value in info.values()):
            response = {'error': 'All fields are required'}
            return jsonify(response)

        try:
            auth_utils.update_personal_info(username, info)
            response = {'message': 'User information updated successfully'}
            return jsonify(response)
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response)

class DisplayPersonalInfo(Resource):
    def get(self, username):
        try:
            user_info = auth_utils.get_personal_info(username)
            if user_info:
                return jsonify(user_info)
            else:
                response = {'error': 'User not found'}
                return jsonify(response)
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response)

class UpdateProfessionalInfo(Resource):
    def post(self, username):
        data = request.get_json()
        professional_info = {
            '12th_percentage': data.get('12th_percentage'),
            'graduation_year': data.get('graduation_year'),
            'degree_pursued': data.get('degree_pursued'),
            'employment_status': data.get('employment_status'),
            'office_name': data.get('office_name'),
            'salary': data.get('salary'),
            'current_designation': data.get('current_designation'),
            'experience': data.get('experience'),
        }

        if any(value is None for value in professional_info.values()):
            response = {'error': 'All fields are required'}
            return jsonify(response)

        try:
            auth_utils.update_professional_info(username, professional_info)
            response = {'message': 'Professional information updated successfully'}
            return jsonify(response)
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response)
class DisplayProfessionalInfo(Resource):
    def get(self, username):
        try:
            prof_info = auth_utils.get_professional_info(username)
            if prof_info:
                return jsonify(prof_info)
            else:
                response = {'error': 'Professional information not found'}
                return jsonify(response)
        except Exception as e:
            response = {'error': str(e)}
            return jsonify(response)

api.add_resource(Register, '/register')
api.add_resource(Authenticate, '/authenticate')
api.add_resource(UpdatePersonalInfo, '/update_personal_info/<username>')
api.add_resource(DisplayPersonalInfo, '/display_personal_info/<username>')
api.add_resource(UpdateProfessionalInfo, '/update_professional_info/<username>')
api.add_resource(DisplayProfessionalInfo, '/display_professional_info/<username>')

if __name__ == '__main__':
    app.run(debug=True)