# importing modules necessary to run application
from flask import Flask
from flask import render_template as render
import mysql.connector


app = Flask(__name__)

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='anand',
    password='pass',
    database='temp_class'
)


# Create a cursor to interact with the database
cursor = db_connection.cursor()

@app.route('/')
@app.route('/home')
def home():
    return render('home.html')

@app.route('dashboard')
def dashboard():
    return "Dashboard page"

@app.route('visualization')
def visualization():
    return "Visualization"


if __name__ == '__main__':
    app.run(debug=True)