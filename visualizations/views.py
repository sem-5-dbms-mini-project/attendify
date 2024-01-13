import os
from django.conf import settings
from django.shortcuts import render, redirect
import mysql.connector
from .utils import attendance as attend
from .utils import ia as ia_marks
from .utils import csv_to_database_tables as csvToDB


# Connect to MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='anand',
    password='pass',
    database='temp_class'
)

# Create your views here.

def home(request):
    return render(request, 'home.html')

def analytics(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['csv_file']

        # Specify the destination folder
        destination_folder = os.path.join(settings.BASE_DIR, 'global')

        # Ensure the destination folder exists, create it if not
        os.makedirs(destination_folder, exist_ok=True)

        # Construct the destination path
        destination_path = os.path.join(destination_folder, uploaded_file.name)

        # Save the file to the destination path
        with open(destination_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Read the CSV file
        csv_file = destination_path
        table_name = csvToDB.studentTableCreation(csv_file, db_connection)

        analytics = attend.runAll(table_name, db_connection)


        db_connection.close()
        return render(request, 'analysis.html', {'analytics':analytics})

    return render(request, 'analysis.html')


# testing git merge