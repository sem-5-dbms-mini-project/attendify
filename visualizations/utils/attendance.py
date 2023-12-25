import os
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import mysql.connector

def createDataframe(table_name, db_connection):
    # Read data from MySQL into a DataFrame
    query = f"SELECT * FROM `{table_name}`"
    df = pd.read_sql(query, con=db_connection)
    return df

def createAnalysisFolder():
    # Specify the destination folder
    destination_path = os.path.join(settings.BASE_DIR, 'global/analysis/attendance')

    # Ensure the destination folder exists, create it if not
    os.makedirs(destination_path, exist_ok=True)

    return destination_path

def attendanceCategories(df, destination_path, visualizations_path):
    # Assuming df is your DataFrame with 'ATTENDANCE PERCENTAGE' column
    labels = ['<75%', '75-85%', '>85%']
    attendance_bins = [0, 75, 85, 100]
    attendance_categories = pd.cut(df['ATTENDANCE PERCENTAGE'], bins=attendance_bins, labels=labels)

    # Pie Chart for Number of Students in Each Attendance Category
    pie_chart_attendance_categories = px.pie(names=attendance_categories, title='Pie Chart for Attendance Categories')
    # pie_chart_attendance_categories.show()
    plotly.offline.plot(pie_chart_attendance_categories, filename=f"{destination_path}/pieChartCategories.html")
    visualizations_path['CategoriesPie'] = f"{destination_path}/pieChartCategories.html"

def pieChart_AttendanceStatus(df, destination_path, visualizations_path):
    attendance_status_labels = ['Low Attendance', 'Moderate Attendance', 'High Attendance']
    attendance_status_bins = [0, 75, 90, 100]
    attendance_status_counts = pd.cut(df['ATTENDANCE PERCENTAGE'], bins=attendance_status_bins, labels=attendance_status_labels).value_counts()

    pie_chart_attendance_status = px.pie(names=attendance_status_counts.index, values=attendance_status_counts.values, title='Pie Chart for Class Attendance Status')
    # pie_chart_attendance_status.show()
    plotly.offline.plot(pie_chart_attendance_status, filename=f"{destination_path}/pieChartStatus.html")
    visualizations_path['StatusPie'] = f"{destination_path}/pieChartStatus.html"

def attendanceBarChart(df, destination_path, visualizations_path):
    # Assuming df is your DataFrame
    bar_chart = px.bar(df, x='STUDENTS NAME', y='ATTENDANCE PERCENTAGE',
                    title='Bar Chart for Attendance',
                    labels={'ATTENDANCE PERCENTAGE': 'Attendance Percentage'},
                    color='STUDENTS NAME')

    # bar_chart.show()
    plotly.offline.plot(bar_chart, filename=f"{destination_path}/AllStudentsAtOnce.html")
    visualizations_path['AllAtOnceBar'] = f"{destination_path}/AllStudentsAtOnce.html"

def attendanceDistributionHistogram(df, destination_path, visualizations_path):
    histogram_attendance_distribution = px.histogram(df, x='ATTENDANCE PERCENTAGE', title='Attendance Distribution Histogram', nbins=20)
    # histogram_attendance_distribution.show()
    plotly.offline.plot(histogram_attendance_distribution, filename=f"{destination_path}/DistributionHistogram.html")
    visualizations_path['DistributionHistogram'] = f"{destination_path}/DistributionHistogram.html"

def barPlotForAbsentees(df, destination_path, visualizations_path):
    # Bar plot of Absent students
    bar_fig = px.bar(df, x='STUDENTS NAME', y='ABSENT', title='Number of Classes Absent')
    bar_fig.update_layout(xaxis=dict(tickangle=45))
    plotly.offline.plot(bar_fig, filename=f"{destination_path}/Absentees.html")
    visualizations_path['AbsenteesBar'] = f"{destination_path}/Absentees.html"

def attendanceBelowCertainNumbers(df, destination_path, visualizations_path):
    # Create a table with USN, student names, attendance percentage, total classes held, and total classes attended
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=['USN/Sr.no', 'Students Name', 'Attendance Percentage', 'Total Classes Held', 'Total Classes Attended']),
        cells=dict(values=[df['SR. NO'], df['STUDENTS NAME'], df['ATTENDANCE PERCENTAGE'],df['TOTAL HELD'], df['TOTAL PRESENT'] ])
    )])

    # Update layout
    table_fig.update_layout(title_text='Students Attendance Table')


    # Filter students with attendance below 75%
    below_75_df = df[df['ATTENDANCE PERCENTAGE'] < 75]

    # Filter students with attendance below 85%
    below_85_df = df[df['ATTENDANCE PERCENTAGE'] < 85]

    # Create a table for students with attendance below 75%
    table_below_75 = go.Figure(data=[go.Table(
        header=dict(values=['USN/SR. NO', 'Students Name', 'Attendance Percentage', 'Total Classes Held', 'Total Classes Attended']),
        cells=dict(values=[below_75_df['SR. NO'], below_75_df['STUDENTS NAME'], below_75_df['ATTENDANCE PERCENTAGE'],
                        below_75_df['TOTAL HELD'], below_75_df['TOTAL PRESENT']])
    )])

    # Update layout
    table_below_75.update_layout(title_text='Students with Attendance Below 75%')

    # Create a table for students with attendance below 85%
    table_below_85 = go.Figure(data=[go.Table(
        header=dict(values=['USN/SR. NO', 'Students Name', 'Attendance Percentage', 'Total Classes Held', 'Total Classes Attended']),
        cells=dict(values=[below_85_df['SR. NO'], below_85_df['STUDENTS NAME'], below_85_df['ATTENDANCE PERCENTAGE'],
                        below_85_df['TOTAL HELD'], below_85_df['TOTAL PRESENT']])
    )])

    # Update layout
    table_below_85.update_layout(title_text='Students with Attendance Below 85%')

    # Show the table
    # table_fig.show()
    # table_below_75.show()
    # table_below_85.show()
    plotly.offline.plot(table_fig, filename=f"{destination_path}/AllStudentsPercentages.html")
    plotly.offline.plot(table_below_75, filename=f"{destination_path}/Below75.html")
    plotly.offline.plot(table_below_85, filename=f"{destination_path}/Below85.html")
    visualizations_path['AllStudentsTable'] = f"{destination_path}/AllStudentsPercentages.html"
    visualizations_path['StudentsBelow75'] = f"{destination_path}/Below75.html"
    visualizations_path['StudentsBelow85'] = f"{destination_path}/Below85.html"

def pieChartForAttendanceRanges(df, destination_path, visualizations_path):
    # Assuming df is your DataFrame with 'ATTENDANCE PERCENTAGE' column
    labels = ['<75%', '75-80%', '80-85%', '85-90%', '90-95%', '95-100%']
    attendance_ranges = pd.cut(df['ATTENDANCE PERCENTAGE'], bins=[0, 75, 80, 85, 90, 95, 100], labels=labels)

    pie_chart_attendance_ranges = px.pie(names=attendance_ranges, title='Pie Chart for Attendance Ranges')
    # pie_chart_attendance_ranges.show()
    plotly.offline.plot(pie_chart_attendance_ranges, filename=f"{destination_path}/pieChartRanges.html")
    visualizations_path['RangesPie'] = f"{destination_path}/pieChartRanges.html"

def classAttendanceStatistics(df, destination_path, visualizations_path):
    class_attendance_stats = df['ATTENDANCE PERCENTAGE'].describe()
    class_attendance_stats_chart = px.bar(x=class_attendance_stats.index, y=class_attendance_stats.values,
                                        labels={'index': 'Statistic', 'value': 'Attendance Percentage'},
                                        title='Class Attendance Statistics')
    # class_attendance_stats_chart.show()
    plotly.offline.plot(class_attendance_stats_chart, filename=f"{destination_path}/ClassStatistics.html")
    visualizations_path['ClassStatisticsBar'] = f"{destination_path}/ClassStatistics.html"

def runAll(table_name, db_connection):
    df = createDataframe(table_name, db_connection)
    destination_path = createAnalysisFolder()
    visualizations_path = {}
    attendanceCategories(df, destination_path, visualizations_path)
    pieChart_AttendanceStatus(df, destination_path, visualizations_path)
    attendanceBarChart(df, destination_path, visualizations_path)
    attendanceDistributionHistogram(df, destination_path, visualizations_path)
    barPlotForAbsentees(df, destination_path, visualizations_path)
    attendanceBelowCertainNumbers(df, destination_path, visualizations_path)
    pieChartForAttendanceRanges(df, destination_path, visualizations_path)
    classAttendanceStatistics(df, destination_path, visualizations_path)
    return visualizations_path


# Below code is just for testing whether the functions work

# df = createDataframe()

# attendanceCategories(df)

# pieChart_AttendanceStatus(df)

# attendanceBarChart(df)

# attendanceDistributionHistogram(df)

# barPlotForAbsentees(df)

# attendanceBelowCertainNumbers(df)

# pieChartForAttendanceRanges(df)

# classAttendanceStatistics(df)