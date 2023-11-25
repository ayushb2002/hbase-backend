from flask import Flask, jsonify
import happybase

app = Flask(__name__)

connection = happybase.Connection("hadoop", 9090, autoconnect=False)

# Test the connection
try:
    connection.open()
    tables = connection.tables()
    print('Connected to HBase. Tables:', tables)
except Exception as e:
    print('Error connecting to HBase:', e)
finally:
    connection.close()
