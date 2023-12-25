import pandas as pd
import numpy as np
import mysql.connector
import os

def studentTableCreation(csv_file_path, db_connection):
    # Read the CSV file, skipping initial rows and using row 3 as header
    df1 = pd.read_csv(csv_file_path, skiprows = 3, usecols = ['Sr. No', 'USN','Students Name'])
    df2 = pd.read_csv(csv_file_path, skiprows = 2, usecols = ['Absent', 'Total Present', 'Total Held', 'IA I', 'IA II', 'IA III', 'Final IA'])

    # Get the course name, faculty name, e-mail and mobile no.
    course_name_index = df1.index[df1["USN"] == "Course Name"]
    faculty_name_index = df1.index[df1["USN"] == "Name of Faculty"]

    course_name = str(df1.iloc[course_name_index, 2][course_name_index[0]])
    faculty_name = str(df1.iloc[faculty_name_index, 2][faculty_name_index[0]])

    # Remove the unnecessary rows which got added in due to structure of csv file
    df1.drop(df1.index[[-1,-2,-3,-4,-5]], inplace=True)

    # Reset the indices of df2
    df2.drop(0, inplace=True)
    reset_indexes = []
    for i in range(0, len(df2)):
        reset_indexes.append(i)
    df2.index = reset_indexes

    df = df1.join(df2)

    # Convert all columns names to uppercase
    df.columns = df.columns.str.upper()

    # Add course name,faculty name and sem column and set the same values for all rows
    sem_df = pd.read_csv(csv_file_path, skiprows = 1, usecols = ["Sem", "Class No"])
    df.insert(2, 'Sem', int(sem_df.iloc[0,0]))
    df['Course Name'] = course_name
    df['Faculty Name'] = faculty_name
    attendance = calculate_attendance_percentage(df)
    df['ATTENDANCE PERCENTAGE'] = attendance

    # Replace 'AB' with NaN in the specified columns
    df['IA I'].replace('AB', None, inplace=True)
    df['IA II'].replace('AB', None, inplace=True)
    df['IA III'].replace('AB', None, inplace=True)

    # Convert columns from text to numeric
    df['IA I'] = pd.to_numeric(df['IA I'], errors='coerce')
    df['IA II'] = pd.to_numeric(df['IA II'], errors='coerce')
    df['IA III'] = pd.to_numeric(df['IA III'], errors='coerce')

    # Replace NaN values wil NULL
    df = df.replace({np.nan: None})

    table_name = "SEM " + str(sem_df.iloc[0,0]) + " " + str(sem_df.iloc[0,1])

    # Create a cursor
    cursor = db_connection.cursor()

    # Drop the table first to ensure there are no duplicates
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

    # Create the table with explicit data types
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (" \
                        f"`SR. NO` INT, " \
                        f"USN VARCHAR(255), " \
                        f"`STUDENTS NAME` VARCHAR(255), " \
                        f"SEM INT, " \
                        f"ABSENT INT, " \
                        f"`TOTAL PRESENT` INT, " \
                        f"`TOTAL HELD` INT, " \
                        f"`ATTENDANCE PERCENTAGE` INT, " \
                        f"`IA I` INT, " \
                        f"`IA II` INT, " \
                        f"`IA III` INT, " \
                        f"`FINAL IA` INT, " \
                        f"`COURSE NAME` VARCHAR(255), " \
                        f"`FACULTY NAME` VARCHAR(255)" \
                        f")"

    cursor.execute(create_table_query)

    # Insert data into the table
    for _, row in df.iterrows():
        insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s' for _ in df.columns])})"
        cursor.execute(insert_query, tuple(row))

    # Commit changes and close the connection
    db_connection.commit()
    cursor.close()

    return table_name

def facultyTableInsertion(csv_file_path, db_connection):
    # Read the CSV file, skipping initial rows and using row 3 as header
    df1 = pd.read_csv(csv_file_path, skiprows = 3, usecols = ['Sr. No', 'USN','Students Name'])

    # Get the course name, faculty name, e-mail and mobile no.
    course_name_index = df1.index[df1["USN"] == "Course Name"]
    faculty_name_index = df1.index[df1["USN"] == "Name of Faculty"]
    faculty_email_index = df1.index[df1["USN"] == "e-mail"]
    faculty_mobile_index = df1.index[df1["USN"] == "Mobile"]

    course_name = str(df1.iloc[course_name_index, 2][course_name_index[0]])
    faculty_name = str(df1.iloc[faculty_name_index, 2][faculty_name_index[0]])
    faculty_email = str(df1.iloc[faculty_email_index, 2][faculty_email_index[0]])
    faculty_mobile = str(df1.iloc[faculty_mobile_index, 2][faculty_mobile_index[0]])

    # df = pd.DataFrame([[faculty_name, course_name, faculty_email, faculty_mobile]], columns = ['FACULTY NAME', 'COURSE NAME', 'E-MAIL', 'MOBILE'])

    # print(df)

    # Create a cursor
    cursor = db_connection.cursor()

    table_name = "faculty_details"

    # Insert data into the table. And if the person already exists then the non unique values are updated
    insert_query = f"INSERT INTO {table_name} VALUES('{faculty_name}', '{course_name}', '{faculty_email}', {faculty_mobile}) ON DUPLICATE KEY UPDATE `E-MAIL` = '{faculty_email}', MOBILE = {faculty_mobile}"

    cursor.execute(insert_query)

    # Commit changes and close the connection
    db_connection.commit()
    cursor.close()
    db_connection.close()

def calculate_attendance_percentage(df):
    """
    Calculate attendance percentage for each student in the DataFrame.

    Parameters:
    - df: pandas DataFrame containing 'Total Present' and 'Total Held' columns.

    Returns:
    - attendance_percentages: List of calculated attendance percentages for each student.
    """

    # Check if the required columns are present in the DataFrame
    if 'TOTAL PRESENT' not in df.columns or 'TOTAL HELD' not in df.columns:
        raise ValueError("The DataFrame must contain 'TOTAL PRESENT' and 'TOTAL HELD' columns.")

    # Calculate attendance percentage for each student
    attendance_percentages = []
    for _, row in df.iterrows():
        total_present = row['TOTAL PRESENT']
        total_held = row['TOTAL HELD']

        # Handle division by zero (if total_held is 0)
        if total_held == 0:
            attendance_percentage = 0.0
        else:
            attendance_percentage = (total_present / total_held) * 100

        # Round the attendance percentage to the nearest whole number
        rounded_percentage = round(attendance_percentage, 0)
        attendance_percentages.append(rounded_percentage)

    return attendance_percentages


# studentTableCreation(csv_file_path, db_connection)

# facultyTableInsertion(csv_file_path, db_connection)