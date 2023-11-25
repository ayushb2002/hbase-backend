import happybase

class AuthUtils:
    def __init__(self, host, port):
        self.connection = happybase.Connection(host, port=port)

    def create_user_table(self):
        # Create an HBase table for storing user information
        self.connection.create_table(
            'users',
            {'info': dict(), 'auth': dict()}
        )

    def get_user(self, username):
        # Get user information from HBase
        table = self.connection.table('users')
        user_data = table.row(username.encode('utf-8'))
        return {key.decode('utf-8'): value.decode('utf-8') for key, value in user_data.items()}

    def add_user(self, username, password):
        # Add a new user to the HBase table
        table = self.connection.table('users')
        table.put(username.encode('utf-8'), {'auth:password': password.encode('utf-8')})
