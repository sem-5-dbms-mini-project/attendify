import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import mysql.connector


def createDataframe(db_connection):
    # Read data from MySQL into a DataFrame
    table_name = "SEM 3 CSE A-3"
    query = f"SELECT * FROM `{table_name}`"
    df = pd.read_sql(query, con=db_connection)
    return df

def IA_pieCharts(df):
    # Assuming df has columns for "IA I", "IA II", and "IA III"
    ia_columns = ["IA I", "IA II", "IA III"]

    for ia_column in ia_columns:
        # Check if the IA column has NaN, empty, or zero values
        if df[ia_column].isnull().all() or (df[ia_column] == 0).all():
            print(f"Skipping {ia_column} as it is Empty/filled with zeros.")
            continue

        # Create a new column indicating the performance category for each IA
        df[f"{ia_column} Category"] = pd.cut(df[ia_column], bins=[-1, 0, 14, 20, 30, 40], labels=["Absent", "Fail", "<20", "20-30", "30-40"])

        # Create a pie chart for the IA category distribution
        pie_chart = px.pie(df, names=f"{ia_column} Category", title=f"{ia_column} Category Distribution", hole=0.3, labels={'<20': '< 20', '30-40': '30 - 40', '20-30': '20 - 30'})

        pie_chart.show()

def IA_boxPlot(df):
    # Visualization 2: Box plot of IA scores
    melted_df = pd.melt(df[['IA I', 'IA II', 'IA III']], var_name='IA Type', value_name='IA Score')
    box_fig = px.box(melted_df, x='IA Type', y='IA Score', title='Boxplot of IA Scores')
    box_fig.show()

def IA_and_attendanceCorrelationHeatmap(df):
    correlation_columns = ['ABSENT', 'TOTAL PRESENT', 'ATTENDANCE PERCENTAGE', 'IA I', 'IA II']

    # Filter out columns with NaN values
    corr_columns = df[correlation_columns].dropna(axis=1, how='all').columns

    # Visualization: Correlation heatmap for specific columns
    corr_fig = px.imshow(df[correlation_columns][corr_columns].corr(), x=corr_columns, y=corr_columns,
                        title='Correlation Heatmap for IA Marks and Attendance')

    # Show the plot
    corr_fig.show()

def performanceDistribution(df):
    # Assuming max marks for both IA I and IA II are 40
    max_marks_ia1 = 40
    max_marks_ia2 = 40

    # Calculate Overall Performance
    df["Overall Performance"] = ((df["IA I"] / max_marks_ia1) + (df["IA II"] / max_marks_ia2)) / 2

    # Check for NaN values in the "Overall Performance" column
    nan_mask = df["Overall Performance"].isna()
    if nan_mask.any():
        print("Warning: NaN values found in 'Overall Performance' column. Handling NaN values.")
        # Handle NaN values, for example, by filling them with a default value
        df["Overall Performance"].fillna(0, inplace=True)

    # Categorize overall performance
    performance_categories = pd.cut(df["Overall Performance"], bins=[0, 0.4, 0.7, 1.0], labels=["Low", "Average", "High"])
    df["Performance Category"] = performance_categories

    # Visualize the distribution of performance categories using Plotly Express
    bar_fig = px.bar(df, x='Performance Category', title='Distribution of Performance Categories',
                    labels={'Performance Category': 'Performance Category', 'count': 'Count'},
                    category_orders={"Performance Category": ["Low", "Average", "High"]})
    bar_fig.update_layout(xaxis_title='Performance Category', yaxis_title='Count')
    bar_fig.show()

def IA_histogram(df):
    # Assuming df has columns "IA I", "IA II", "IA III"
    filtered_df = df[['IA I', 'IA II', 'IA III']].replace({0: None}).dropna(axis=1, how='all')
    hist_fig = px.histogram(filtered_df, x=filtered_df.columns, nbins=10, title='Histogram for IA Scores')
    hist_fig.show()

def IA_average(df):
    # Assuming df has columns "IA I", "IA II", "IA III"
    filtered_df = df[['IA I', 'IA II', 'IA III']].replace({0: None}).dropna(axis=1, how='all')
    avg_ia_scores = filtered_df.mean().reset_index(name='Average Score')
    bar_fig = px.bar(avg_ia_scores, x='index', y='Average Score', title='Average IA Scores',
                    labels={'index': 'IA', 'Average Score': 'Average Score'})
    bar_fig.show()

# Below code is just for testing whether the functions work

# df = createDataframe()

# IA_pieCharts(df)

# IA_boxPlot(df)

# IA_and_attendanceCorrelationHeatmap(df)

# performanceDistribution(df)

# IA_histogram(df)

# IA_average(df)