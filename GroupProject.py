import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st
import numpy as np

color = sns.color_palette()
plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['figure.dpi'] = 100

# Read the CSV file into a DataFrame
df1 = pd.read_csv('healthcare-dataset-stroke-data.csv')
#display the first 5 of first dataset
df1.head()

df2 = pd.read_csv('Stroke data Malaysian.csv')
#display the first 5 of second dataset
df2.head()

df3 = pd.read_csv('aa.csv')
#display the first 5 of third dataset
df3.head()

#display statistical information about first dataset
df1.describe()

#display statistical information about second dataset
df2.describe()

#display statistical information about third dataset
df3.describe()

# Filter out the "children" and "never_worked" categories from the 'work_type' attribute
filtered_data = df1[(df1['work_type'] != 'children') & (df1['work_type'] != 'Never_worked')]

# Group the filtered data by 'work_type' and 'residence_type' and calculate the sum of 'stroke' occurrences
grouped_data = filtered_data.groupby(['work_type', 'Residence_type'])['stroke'].sum().unstack()

# Sort the grouped data by stroke occurrences in descending order
sorted_data = grouped_data.sum(axis=1).sort_values(ascending=False)

# Reorder the rows in the grouped data based on the sorted data
grouped_data = grouped_data.loc[sorted_data.index]

fig1 = go.Figure()

# Define the colors for each cluster
colors = ['#FC7676', '#722F37']

for i, col in enumerate(grouped_data.columns):
    fig1.add_trace(go.Bar(
        x=grouped_data.index,
        y=grouped_data[col],
        name=col,
        marker_color=colors[i % len(colors)]  # Set the color for each cluster
    ))

fig1.update_layout(
    title={
        'text': 'Which Residence Type has the Most Stroke Cases by Work Type?',
        'font': {'size': 24},
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Work Type',
    yaxis_title='Number of Stroke Cases',
    legend=dict(title='Residence Type'),
)

# Show the chart
fig1.show()

# Filter the data for stroke occurrences
stroke_data = df1[df1['stroke'] == 1]

# Count the stroke occurrences by marital status
marital_status_counts = stroke_data['ever_married'].value_counts()

# Extract the values from the Series
values = marital_status_counts.values

# Define the colors for the pie slices
colors = ['#FF9999', '#66B2FF']

fig2 = go.Figure(data=[go.Pie(labels=None, values=marital_status_counts.values)])
fig2.update_layout(
    title={
        'text': 'Distribution of Stroke Cases by Marital Status',
        'font': {'size': 24},
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top'
    },
)

# Set the legend labels
legend_labels = ['Not Married', 'Married']
fig2.update_traces(
    hoverinfo='label+percent',
    textfont_size=12,
    marker=dict(colors=colors),
    labels=legend_labels,
    automargin=True  # Use 'automargin' instead of 'itemSizing'
)

# Add the legend
fig2.update_layout(
    legend=dict(
        title='Marital Status'
    )
)

# Show the chart
fig2.show()

# Count the occurrences of each unique value in avg_glucose_level for each bmi value
counts = df1.groupby('bmi')['avg_glucose_level'].count()

# Create a bar plot of the counts
fig3 = go.Figure(data=[go.Scatter(x=counts.index, y=counts.values, mode='markers', marker=dict(symbol='circle', size=8, color='cyan'))])

fig3.update_layout(
    title='Sum of Average Glucose Level for each BMI',
    xaxis_title='Body Mass Index',
    yaxis_title='Count',
    legend=dict(title=None)
)

# Display the plot
fig3.show()

# Define stress level categories
stress_levels = ['Rarely', 'Sometimes', 'Always']

# Specify the desired order for sleep duration
sleep_duration_order = ['1 - 3 hours', '4 - 6 hours', '7 - 9 hours']

# Convert sleep duration to a categorical data type with the specified order
df2['sleep_duration'] = pd.Categorical(df2['sleep_duration'], categories=sleep_duration_order, ordered=True)

# Calculate average age for each combination of sleep duration and stress level
grouped_df = df2.groupby(['sleep_duration', 'stress_level'])['age'].mean().reset_index()

# Create line charts for each stress level
fig4 = go.Figure()
for stress_level in stress_levels:
    filtered_df = grouped_df[grouped_df['stress_level'] == stress_level]
    fig4.add_trace(go.Scatter(x=filtered_df['sleep_duration'], y=filtered_df['age'], name=stress_level))
fig4.update_layout(
    title={
        'text': 'Can Sleep Duration and Stress Level Impact Stroke Risk?',
        'font': {'size': 24},
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Sleep Duration',
    yaxis_title='Average Age',
    legend=dict(title='Stress Level')
)

# Display the chart
fig4.show()

# Group the data by sugary_food and gender, and sum the exercise_frequency
grouped_data = df2.groupby(['sugary_intake', 'gender'])['exercise_duration'].sum().unstack()

fig5 = go.Figure()

for col in grouped_data.columns:
    fig5.add_trace(go.Bar(
        x=grouped_data.index,
        y=grouped_data[col],
        name=col
    ))

fig5.update_layout(
    title='Exercise Frequency by Sugary Food and Gender',
    xaxis_title='Sugary Food',
    yaxis_title='Exercise Frequency',
    barmode='stack',
    legend=dict(title='Gender')
)

fig5.show()

years = df3['year'].unique()   # Get unique years
districts = df3['NEGERI'].unique()  # Get unique districts
cases_total = {}

# Iterate over the years
for year in years:
    # Filter the data for each year
    year_data = df3[df3['year'] == year]
    
    for district in districts:
        case = year_data[year_data['NEGERI'] == district]['case'].sum()
        if district in cases_total:
            cases_total[district] += case
        else:
            cases_total[district] = case

# Sort the districts based on the total number of cases in descending order
sorted_districts = sorted(cases_total, key=cases_total.get, reverse=True)

cases = []

# Iterate over the years
for year in years:
    # Filter the data for each year
    year_data = df3[df3['year'] == year]
    
    # Get the cases for each district in the sorted order
    cases_year = [year_data[year_data['NEGERI'] == district]['case'].sum() for district in sorted_districts]
    cases.append(cases_year)

fig6 = go.Figure()

for case_year, year in zip(cases, years):
    fig6.add_trace(go.Scatter(
        x=sorted_districts,
        y=case_year,
        mode='lines',
        fill='tozeroy',
        name=str(year)
    ))

fig6.update_layout(
    title='Number of Cases by District and Year',
    xaxis_title='District',
    yaxis_title='Number of Cases',
    legend=dict(title='Year'),
    xaxis_tickangle=-90
)

fig6.show()

# Function to run ngrok and get the public URL
def get_ngrok_url(port):
    ngrok_cmd = ['ngrok', 'http', str(port)]
    ngrok_process = subprocess.Popen(ngrok_cmd, stdout=subprocess.PIPE)
    
    # Wait for ngrok to generate the public URL
    while True:
        line = ngrok_process.stdout.readline().decode().strip()
        if 'Forwarding' in line:
            url = line.split(' ')[1]
            return url

# Define the page layout for Dashboard 1
def dashboard1():
    st.markdown("<h1 style='text-align: left; margin-bottom: 50px;'>Stroke Analysis and Risk Factors</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig4)

# Define the page layout for Dashboard 2
def dashboard2():
    st.markdown("<h1 style='text-align: center; margin-bottom: 50px;'>Health Metrics and Lifestyle Analysis</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig3)
    st.plotly_chart(fig5)

# Define the page layout for Dashboard 3
def dashboard3():
    st.markdown("<h1 style='text-align: center; margin-bottom: 50px;'>Stroke Analysis by Geographic Distribution</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig1)
    st.plotly_chart(fig6)

# Create a select box to switch between dashboards
dashboard_selection = st.sidebar.selectbox('Select Dashboard', ('Stroke Analysis and Risk Factors', 'Health Metrics and Lifestyle Analysis', 'Stroke Analysis by Geographic Distribution'))

# Show the selected dashboard based on the selection
if dashboard_selection == 'Stroke Analysis and Risk Factors':
    dashboard1()
elif dashboard_selection == 'Health Metrics and Lifestyle Analysis':
    dashboard2()
elif dashboard_selection == 'Stroke Analysis by Geographic Distribution':
    dashboard3()
