import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector

def createDataframe(table_name, db_connection):
    # Read data from MySQL into a DataFrame
    query = f"SELECT * FROM `{table_name}`"
    df = pd.read_sql(query, con=db_connection)
    return df


def createAnalytics(df, table_name, cursor):
    attendanceAnalytics = []

    # Assuming df is your DataFrame with 'ATTENDANCE PERCENTAGE' column
    labels_categories = ['<75%', '75-85%', '>85%']
    attendance_bins_categories = [0, 75, 85, 100]
    attendance_categories = pd.cut(df['ATTENDANCE PERCENTAGE'], bins=attendance_bins_categories, labels=labels_categories)

    # Create visually appealing pie chart for attendance categories using Plotly Express
    pie_chart_attendance_categories = px.pie(
        names=attendance_categories,
        title='Pie Chart for Attendance Categories',
        color_discrete_sequence=px.colors.qualitative.Plotly,  # Set color sequence
    )

    # Update layout for a visually appealing pie chart
    pie_chart_attendance_categories.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),  # Adjust margins for better layout
        paper_bgcolor='rgba(0,0,0,0)',  # Make the background transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Make the plot area background transparent
    )

    # Create bar chart for attendance status using Plotly Graph Objects
    attendance_status_labels = ['Low Attendance', 'Moderate Attendance', 'High Attendance']
    attendance_status_bins = [0, 75, 90, 100]
    attendance_status_counts = pd.cut(df['ATTENDANCE PERCENTAGE'], bins=attendance_status_bins, labels=attendance_status_labels).value_counts()

    bar_chart_attendance_status = go.Figure(
        data=[go.Bar(x=attendance_status_counts.index, y=attendance_status_counts.values)],
    )

    # Update layout for the bar chart
    bar_chart_attendance_status.update_layout(
        title='Bar Chart for Class Attendance Status',
        xaxis_title='Attendance Status',
        yaxis_title='Number of Students',
        margin=dict(l=20, r=20, t=50, b=20),  # Adjust margins for better layout
        paper_bgcolor='rgba(0,0,0,0)',  # Make the background transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Make the plot area background transparent
    )

    # Perform data analysis and create the additional pie chart
    attendance_status_labels = ['Low', 'Moderate', 'High']
    attendance_status_bins = [0, 75, 90, 100]
    attendance_status_counts = pd.cut(df['ATTENDANCE PERCENTAGE'], bins=attendance_status_bins, labels=attendance_status_labels).value_counts()

    # Create additional pie chart using Plotly Graph Objects
    pie_chart_attendance_status = go.Figure(
        data=[go.Pie(labels=attendance_status_counts.index, values=attendance_status_counts.values)],
    )

    # Update layout for the additional pie chart
    pie_chart_attendance_status.update_layout(
        title='Pie Chart for Class Attendance Status',
        margin=dict(l=20, r=20, t=50, b=20),  # Adjust margins for better layout
        paper_bgcolor='rgba(0,0,0,0)',  # Make the background transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Make the plot area background transparent
    )

    # Create histogram for attendance distribution using Plotly Express
    histogram_attendance_distribution = px.histogram(
        df,
        x='ATTENDANCE PERCENTAGE',
        title='Attendance Distribution Histogram',
        nbins=20,
    )

    # Update layout for the histogram
    histogram_attendance_distribution.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),  # Adjust margins for better layout
        paper_bgcolor='rgba(0,0,0,0)',  # Make the background transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Make the plot area background transparent
    )

    # Save the plots as HTML
    pie_chart_html = pie_chart_attendance_categories.to_html(full_html=False, config = {'displayModeBar': False})
    bar_chart_html = bar_chart_attendance_status.to_html(full_html=False, config = {'displayModeBar': False})
    additional_pie_chart_html = pie_chart_attendance_status.to_html(full_html=False, config = {'displayModeBar': False})
    histogram_html = histogram_attendance_distribution.to_html(full_html=False, config = {'displayModeBar': False})

    attendanceAnalytics.extend([pie_chart_html, bar_chart_html, additional_pie_chart_html, histogram_html])

    # tables below

    # Fetch data for all students
    cursor.execute(f"SELECT `SR. NO`, `STUDENTS NAME`, `ATTENDANCE PERCENTAGE`, `TOTAL HELD`, `TOTAL PRESENT` FROM `{table_name}`")
    data = cursor.fetchall()

    # Fetch data for students with attendance less than 85%
    cursor.execute(f"SELECT `SR. NO`, `STUDENTS NAME`, `ATTENDANCE PERCENTAGE`, `TOTAL HELD`, `TOTAL PRESENT` FROM `{table_name}` WHERE `ATTENDANCE PERCENTAGE` < 85")
    data_below_85 = cursor.fetchall()

    # Fetch data for students with attendance less than 75%
    cursor.execute(f"SELECT `SR. NO`, `STUDENTS NAME`, `ATTENDANCE PERCENTAGE`, `TOTAL HELD`, `TOTAL PRESENT` FROM `{table_name}` WHERE `ATTENDANCE PERCENTAGE` < 75")
    data_below_75 = cursor.fetchall()

    attendanceAnalytics.extend([data, data_below_75, data_below_85])

    return attendanceAnalytics



def runAll(table_name, db_connection, cursor):
    df = createDataframe(table_name, db_connection)
    attendanceAnalytics = createAnalytics(df, table_name, cursor)

    return attendanceAnalytics
