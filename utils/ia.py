import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector


def createDataframe(db_connection):
    # Read data from MySQL into a DataFrame
    table_name = "SEM 3 CSE A-3"
    query = f"SELECT * FROM `{table_name}`"
    df = pd.read_sql(query, con=db_connection)
    return df

def createInternalsAnalytics(df):
    # list with all the ia marks visualizations
    iaMarksCharts = []

    # Assuming df has columns for "IA I", "IA II", and "IA III"
    ia_columns = ["IA I", "IA II", "IA III"]

    charts = []

    for ia_column in ia_columns:
        # Check if the IA column has NaN, empty, or zero values
        if df[ia_column].isnull().all() or (df[ia_column] == 0).all():
            print(f"Skipping {ia_column} as it is Empty/filled with zeros.")
            continue

        # Create a new column indicating the performance category for each IA
        df[f"{ia_column} Category"] = pd.cut(df[ia_column], bins=[-1, 0, 14, 20, 30, 40],
                                             labels=["Absent", "Fail", "<20", "20-30", "30-40"])

        # Create a pie chart for the IA category distribution
        fig = px.pie(df, names=f"{ia_column} Category", title=f"{ia_column} Category Distribution",
                     hole=0.3, labels={'<20': '< 20', '30-40': '30 - 40', '20-30': '20 - 30'})

        # Convert the plot to HTML
        chart_html = fig.to_html(full_html=False, config = {'displayModeBar': False})

        charts.append(chart_html)

    # Visualization 2: Box plot of IA scores
    melted_df = pd.melt(df[['IA I', 'IA II', 'IA III']], var_name='IA Type', value_name='IA Score')
    box_fig = px.box(melted_df, x='IA Type', y='IA Score', title='Boxplot of IA Scores')

    # Convert the plot to HTML
    box_html = box_fig.to_html(full_html=False, config = {'displayModeBar': False})

    # Visualization 3: Correlation heatmap for IA Marks and Attendance
    correlation_columns = ["IA I", "IA II", "IA III", "ATTENDANCE PERCENTAGE"]
    corr_fig = px.imshow(df[correlation_columns].corr(), x=correlation_columns, y=correlation_columns,
                         title='Correlation Heatmap for IA Marks and Attendance')

    # Convert the plot to HTML
    corr_html = corr_fig.to_html(full_html=False, config = {'displayModeBar': False})

    iaMarksCharts.append(charts)
    iaMarksCharts.append(box_html)
    iaMarksCharts.append(corr_html)

    return iaMarksCharts

def runAll(table_name, db_connection):
    df = createDataframe(db_connection)
    iaMarksAnalytics = createInternalsAnalytics(df)

    return iaMarksAnalytics
