import happybase
import time

class AuthUtils:
    def __init__(self, host, port):
        self.connection = happybase.Connection(host, port=port)

    def create_user_table(self):
        # Create an HBase table for storing user information
        self.connection.create_table(
            'users',
            {'info': dict(), 'auth': dict(), 'prof': dict()}
        )

    def get_user(self, username):
        # Get user information from HBase
        table = self.connection.table('users')
        user_data = table.row(username.encode('utf-8'))
        return {key.decode('utf-8'): value.decode('utf-8') for key, value in user_data.items()}

    def add_user(self, username, password, employee):
        # Add a new user to the HBase table
        table = self.connection.table('users')
        columns = {
            'auth:password': password.encode('utf-8'),
            'info:verified': 'false'.encode('utf-8'),
            'prof:verified': 'false'.encode('utf-8'),
            'auth:employee': 'true'.encode('utf-8') if employee == 'true' else 'false'.encode('utf-8')
        }
        table.put(username.encode('utf-8'), columns)

    def update_personal_info(self, username, info):
        # Update user information in the HBase table
        timestamp = int(time.time())
        table = self.connection.table('users')
        columns = {'info:' + key: str(value).encode('utf-8') for key, value in info.items()}
        columns['info:timestamp'] = str(timestamp).encode('utf-8')
        columns['info:verified'] = 'false'.encode('utf-8')
        table.put(username.encode('utf-8'), columns)

    def get_personal_info(self, username):
        # Get user information from the HBase table
        table = self.connection.table('users')
        user_info = table.row(username.encode('utf-8'), columns=[b'info:name', b'info:gender', b'info:phone_number', b'info:address', b'info:age', b'info:email'])
        return {key.decode('utf-8').split(':')[1]: value.decode('utf-8') for key, value in user_info.items()}
    
    def update_professional_info(self, username, professional_info):
        # Update professional information in the HBase table
        timestamp = int(time.time())
        table = self.connection.table('users')
        columns = {'prof:' + key: str(value).encode('utf-8') for key, value in professional_info.items()}
        columns['prof:timestamp'] = str(timestamp).encode('utf-8')
        columns['prof:verified'] = 'false'.encode('utf-8')
        table.put(username.encode('utf-8'), columns)

    def get_professional_info(self, username):
        # Get professional information from the HBase table
        table = self.connection.table('users')
        prof_info = table.row(username.encode('utf-8'), columns=[b'prof:12th_percentage', b'prof:graduation_year', b'prof:degree_pursued', b'prof:employment_status', b'prof:office_name', b'prof:salary', b'prof:current_designation', b'prof:experience'])
        return {key.decode('utf-8').split(':')[1]: value.decode('utf-8') for key, value in prof_info.items()}
    
    def get_recent_submissions(self, employee):
        # Get profile submissions in the last 24 hours
        table = self.connection.table('users')
        user_exists = table.row(employee.encode('utf-8'))
        if not user_exists:
            return 'false'
        
        is_employee_filter = f"SingleColumnValueFilter('auth', 'employee', =, 'binary:true', true, false)"
        is_employee = table.scan(row_prefix=employee.encode('utf-8'), filter=is_employee_filter)

        if not any(is_employee):
            return 'false'
        
        current_timestamp = int(time.time())
        last_24_hours = current_timestamp - (24 * 60 * 60)
        scan_filter = f"SingleColumnValueFilter('info', 'timestamp', <=, 'binary:{current_timestamp}', true, false) AND SingleColumnValueFilter('info', 'timestamp', >, 'binary:{last_24_hours}', true, false)"
        scan = self.connection.table('users').scan(filter=scan_filter)
        submissions = []

        for key, data in scan:
            username = key.decode('utf-8')
            timestamp = int(data[b'info:timestamp'].decode('utf-8'))
            submissions.append({'username': username, 'timestamp': timestamp})

        return submissions
    
    def get_user_profile(self, username):
        # Get user profile information from the HBase table
        table = self.connection.table('users')
        profile_info = table.row(username.encode('utf-8'), columns=[b'info', b'prof'])
        return {
            key.decode('utf-8').split(':')[1]: value.decode('utf-8') for key, value in profile_info.items()
        }
    
    def mark_profile_as_verified(self, username):
        # Mark the profile as verified
        table = self.connection.table('users')
        info_columns = {'info:verified': 'true'.encode('utf-8')}
        prof_columns = {'prof:verified': 'true'.encode('utf-8')}
        table.put(username.encode('utf-8'), {**info_columns, **prof_columns})