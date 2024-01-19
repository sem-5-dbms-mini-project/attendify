# importing modules necessary to run application
import os
from flask import Flask, request
from flask import render_template as render
import mysql.connector

# importing visualization related modules
import pandas as pd
from utils import attendance as attend
from utils import ia as ia_marks
from utils import csv_to_database_tables as csvToDB


app = Flask(__name__)

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host='Abhijnans-MacBook-Pro.local',
    user='root',
    password='189@2003ihba',
    database='temp_class2'
)


# Create a cursor to interact with the database
cursor = db_connection.cursor()

filePaths = []
tableNames = []

@app.route('/')
@app.route('/home')
def home():
    return render('home.html')

@app.route('/dashboard/', methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        csv_file = request.files['classCsvFile']
        csv_file.save(os.path.join('static', csv_file.filename))
        csv_file_path = os.path.join('static',csv_file.filename)
        table_name = csvToDB.studentTableCreation(csv_file_path, db_connection)

        filePaths.append(csv_file_path)
        tableNames.append(table_name)

        # get table details to show to user        
        # query = f"SELECT * FROM `{table_name}`"
        # cursor.execute(query)

        # Fetch attendance data for all students
        cursor.execute(f"SELECT `SR. NO`, `STUDENTS NAME`, `ATTENDANCE PERCENTAGE`, `TOTAL HELD`, `TOTAL PRESENT` FROM `{table_name}`")
        tableDisplayedToUser = cursor.fetchall()

        return render('dashboard.html', classTable=tableDisplayedToUser)

    return render('dashboard.html', classTable=None)

@app.route('/visualization')
def visualization():
    print(tableNames)
    attendanceAnalytics = attend.runAll(tableNames[0], db_connection, cursor)
    iaMarksAnalytics = ia_marks.runAll(tableNames[0],db_connection)

    return render('visualization.html', attendanceAnalytics = attendanceAnalytics, iaMarksAnalytics = iaMarksAnalytics)


if __name__ == '__main__':
    app.run(debug=True)