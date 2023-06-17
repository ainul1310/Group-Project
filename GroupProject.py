import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st
import numpy as np

color = sns.color_palette()

# Set the Streamlit app theme to 'wide'
st.set_page_config(layout="wide")

# Customize the theme and background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #EE6B6E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Read the CSV file into a DataFrame
df1 = pd.read_csv('healthcare-dataset-stroke-data.csv')
df2 = pd.read_csv('Stroke data Malaysian.csv')
df3 = pd.read_csv('aa.csv')

# Chart 1

# Filter out the "children" and "never_worked" categories from the 'work_type' attribute
filtered_data = df1[(df1['work_type'] != 'children') & (df1['work_type'] != 'Never_worked')]

# Group the filtered data by 'work_type' and 'residence_type' and calculate the sum of 'stroke' occurrences
grouped_data = filtered_data.groupby(['work_type', 'Residence_type'])['stroke'].sum().unstack()

# Sort the grouped data by stroke occurrences in descending order
sorted_data = grouped_data.sum(axis=1).sort_values(ascending=False)

# Reorder the rows in the grouped data based on the sorted data
grouped_data = grouped_data.loc[sorted_data.index]

# Define the colors for the chart
rural_color = '#FC7676'
urban_color = '#722F37'
other_color_rural = 'lightgray'  # Grey color for rural bars
other_color_urban = 'darkgrey'  # Grey color for urban bars

# Find the maximum stroke cases for rural and urban areas
max_rural_cases = grouped_data.loc[:, 'Rural'].max()
max_urban_cases = grouped_data.loc[:, 'Urban'].max()

# Create the chart bars
bars = []
for col in grouped_data.columns:
    bar_color = [
        rural_color if (x == max_rural_cases and col == 'Rural') else
        urban_color if (x == max_urban_cases and col == 'Urban') else
        other_color_rural if col == 'Rural' else
        other_color_urban
        for x in grouped_data[col]
    ]

    bars.append(go.Bar(
        x=grouped_data.index,
        y=grouped_data[col],
        name=col,
        marker=dict(color=bar_color)
    ))

fig1 = go.Figure(data=bars)

fig1.update_layout(
    paper_bgcolor='#262730',  # Set the background color of the chart
    plot_bgcolor='rgba(0, 0, 0, 0)'  # Set the background color of the plot area to transparent
)

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

# Chart 2

# Filter the data for stroke occurrences
stroke_data = df1[df1['stroke'] == 1]

# Count the stroke occurrences by marital status
marital_status_counts = stroke_data['ever_married'].value_counts()

# Extract the values from the Series
values = marital_status_counts.values

# Define the colors for the pie slices
colors = ['#FC7676', '#722F37']

fig2 = go.Figure(data=[go.Pie(labels=None, values=marital_status_counts.values)])

fig2.update_layout(
    paper_bgcolor='#262730',  # Set the background color of the chart
    plot_bgcolor='rgba(0, 0, 0, 0)'  # Set the background color of the plot area to transparent
)

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
legend_labels = ['Married', 'Not Married']
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

# Chart 3

# Filter the data to include only BMI values up to 60
filtered_data = df1[df1['bmi'] <= 60]

# Calculate the average of avg_glucose_level for each bmi value
averages = filtered_data.groupby('bmi')['avg_glucose_level'].mean()

# Create a bar plot of the averages
fig3 = go.Figure(data=[go.Scatter(x=averages.index, y=averages.values, mode='markers', marker=dict(symbol='circle', size=8, color='#D23B5F'))])

fig3.update_layout(
    paper_bgcolor='#262730',  # Set the background color of the chart
    plot_bgcolor='rgba(0, 0, 0, 0)'  # Set the background color of the plot area to transparent
)

fig3.update_layout(
    title='Did BMI affect the Average Glucose Level?',
    xaxis_title='Body Mass Index',
    yaxis_title='Average Glucose Level',
    legend=dict(title=None),
    font=dict(
        color='white'
    )
)

fig3.update_xaxes(tickfont=dict(color='white'))
fig3.update_yaxes(tickfont=dict(color='white'))

# Chart 4

# Define the desired order for stress levels
stress_level_order = ['Rarely', 'Sometimes', 'Always']

# Specify the desired order for gender
gender_order = ['Male', 'Female']

# Convert stress level to a categorical data type with the specified order
df2['stress_level'] = pd.Categorical(df2['stress_level'], categories=stress_level_order, ordered=True)

# Count the occurrences of each combination of stress level and gender
grouped_df = df2.groupby(['stress_level', 'gender']).size().reset_index(name='total')

# Create line charts for each gender
fig4 = go.Figure()
for gender in gender_order:
    filtered_df = grouped_df[grouped_df['gender'] == gender]
    fig4.add_trace(go.Scatter(x=filtered_df['stress_level'], y=filtered_df['total'], name=gender))

fig4.update_layout(
    paper_bgcolor='#262730',  # Set the background color of the chart
    plot_bgcolor='rgba(0, 0, 0, 0)'  # Set the background color of the plot area to transparent
)

# Set chart title and axis labels
fig4.update_layout(
    title={
        'text': 'How Does Gender Influence Stress Levels?',
        'font': {'size': 24},
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title='Stress Level',
    yaxis_title='Total',
    legend=dict(title='Gender')
)

# Chart 5

# Group the data by sugary_food and gender, and sum the exercise_frequency
# Group the data by sugary_intake and gender, and calculate the mean of exercise_duration
grouped_data = df2.groupby(['sugary_intake', 'gender'])['exercise_duration'].mean().unstack()

# Define the colors for the bars
colors = []

for intake in grouped_data.index:
    if intake in ['1-2 times', '5-6 times', '7-8 times']:
        colors.extend(['grey', 'lightgrey'])
    elif intake == '3-4 times':
        colors.extend(['red', '#FF7276'])

fig5 = go.Figure()

for i, col in enumerate(grouped_data.columns):
    fig5.add_trace(go.Bar(
        x=grouped_data.index,
        y=grouped_data[col],
        name=col,
        marker=dict(color=colors[i::len(grouped_data.columns)])  # Set the color for each bar
    ))

fig5.update_layout(
    paper_bgcolor='#262730',  # Set the background color of the chart
    plot_bgcolor='rgba(0, 0, 0, 0)'  # Set the background color of the plot area to transparent
)

fig5.update_layout(
    title='Which gender and how much sugar intake has the highest average exercise per week?',
    xaxis_title='Sugary Intake in Week',
    yaxis_title='Average Exercise in Week',
    barmode='stack',
    legend=dict(title='Gender')
)
fig5.update_xaxes(tickfont=dict(color='white'))
fig5.update_yaxes(tickfont=dict(color='white'))

# Chart 6

years = df3['year'].unique()
states = df3['NEGERI'].unique()

cases_total = {}

# Calculate the total cases for each state
for state in states:
    case = df3[df3['NEGERI'] == state]['case'].sum()
    cases_total[state] = case

# Sort the states based on the total number of cases in descending order
sorted_states = sorted(cases_total, key=cases_total.get, reverse=True)

cases = []

# Iterate over the years
for year in years:
    # Filter the data for each year
    year_data = df3[df3['year'] == year]

    # Get the cases for each state in the sorted order
    cases_year = [year_data[year_data['NEGERI'] == state]['case'].sum() for state in sorted_states]
    cases.append(cases_year)

colors = ['#FF9696', 'red', 'darkred']

fig6 = go.Figure()

for i, year in enumerate(years):
    fig6.add_trace(go.Scatter(
        x=sorted_states,
        y=cases[i],
        mode='lines',
        stackgroup='one',
        name=str(year),
        line=dict(color=colors[i])
    ))

fig6.update_layout(
    paper_bgcolor='#262730',  # Set the background color of the chart
    plot_bgcolor='rgba(0, 0, 0, 0)'  # Set the background color of the plot area to transparent
)

fig6.update_layout(
    title='How Do Stroke Cases Evolve Over Time in Different States?',
    xaxis_title='State',
    yaxis_title='Number of Cases',
    showlegend=True
)

# Define the page layout for Dashboard 1
def dashboard1():
    st.markdown("<h1 style='text-align: center; margin-bottom: 50px; text-decoration: underline;'>Stroke Analysis and Risk Factors</h1>", unsafe_allow_html=True)
    
    # Create two columns for the figures and descriptions
    col1, col2 = st.columns([2, 1])
    
    # Display the first figure and its description
    with col1:
        st.plotly_chart(fig1)
    with col2:
        st.markdown("<p style='font-size: 20px;text-align: justify;'>Private jobs have been associated with a higher incidence of stroke, with 66 cases reported in urban areas and 61 cases in rural areas.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 20px;text-align: justify;'>Private employment frequently entails high-stress settings with demanding workloads, constrained deadlines, and lengthy workdays.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 20px;text-align: justify;'>Employees in private sector occupations sometimes spend lengthy periods of time sitting at a desk or in front of a computer, doing little or no physical exercise.</p>", unsafe_allow_html=True)
    
    # Display the second figure and its description
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.plotly_chart(fig2)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<p style='font-size: 20px;text-align: justify;'>The analysis reveals that the majority of stroke cases (89%) occurred among married individuals, while only a small proportion (11%) were reported among unmarried individuals.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 20px;text-align: justify;'>Relationship problems and caregiving obligations are only two stressors that being married may bring about."
                    " These stressors can raise stress levels and may even increase the risk of stroke.</p>", unsafe_allow_html=True)
    
    # Display the third figure and its description
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.plotly_chart(fig4)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<p style='font-size: 20px;text-align: justify;'>Based on the chart, it is observed that females experience higher levels of stress compared to males." 
                    " It is important to note that stress is a known risk factor for stroke.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 20px;text-align: justify;'>Females could have particular socioeconomic obstacles including childcare duties, work-life balance, and gender inequality at work."
                    " They may experience more stress due to hormonal changes, notably those that occur during menstruation, pregnancy, and menopause.</p>", unsafe_allow_html=True)
    
    # Add a line at the bottom
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    st.markdown("<p style='font-size: 20px;text-align: justify;'>Combining these claims, the study implies that variances in stroke risk may be influenced by elements including stress from one's job, marital status, and gender differences in stress levels."
                " It emphasises how crucial it is to deal with stress management and encourage social support networks in order to reduce stroke risk factors.</p>", unsafe_allow_html=True)

# Define the page layout for Dashboard 2
def dashboard2():
    st.markdown("<h1 style='text-align: center; margin-bottom: 50px; text-decoration: underline;'>Health Metrics and Lifestyle Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
    "<p style='font-size: 21px;text-align: justify;'>The scatter plot and column chart are the two charts that make up this dashboard. "
    + 'The first graph, a scatter plot illustrates the relationship between the average'
    + ' blood glucose level with body mass index (BMI). The relationship between total weekly exercise, sugar consumption, '
    + 'and gender is illustrated in the second chart, which is a column chart.',
    unsafe_allow_html=True
    )
    st.markdown("---")

    # Create two columns for the figures and descriptions
    col1, col2 = st.columns([1.2, 2])
    
    # Display the first figure and its description
    with col1:
       st.write("")
       st.write("")
       st.write("")
       st.markdown("<p style='font-size: 21px;text-align: justify;'>The chart shows that the average glucose level increases as BMI increases.</p>", unsafe_allow_html=True)
       st.markdown("<p style='font-size: 21px;text-align: justify;'>This might be because of insulin resistance, a condition where the body's cells become less responsive to "
                   + "the effects of insulin, is frequently linked to higher BMI. Blood glucose levels are controlled by insulin, and when cells become resistant to insulin, "
                   + "glucose may build up in the bloodstream and cause glucose levels to rise.</p>", unsafe_allow_html=True)
       st.markdown("<p style='font-size: 21px;text-align: justify;'> However, there is still some of the record that not consistent which may be due to a number of factors such as "
                   "family history, lifestyle choices, and general health state.</p>", unsafe_allow_html=True)
    with col2:
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.plotly_chart(fig3)
       
    with col1:
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.markdown("<p style='font-size: 21px;text-align: justify;'>Three to four times sugary intake recorded the highest average of exercise in a week  </p>", unsafe_allow_html=True)
       st.markdown("<p style='font-size: 21px;text-align: justify;'>We can see that male are more active in exercise compare to female."
                   " This might be because of males often have more muscular mass and testosterone in their bodies, which can lead to increased strength and athletic performance. </p>", unsafe_allow_html=True)
       st.markdown("<p style='font-size: 21px;text-align: justify;'>From this chart we see that students at UiTM practice a healthy lifestyle with most of them consuming sugary foods "
                   "only three to four times a week following the highest exercise rate. </p>", unsafe_allow_html=True)
      
    with col2:
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.plotly_chart(fig5)

    # Add a line
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px;text-align: justify;'>From the two charts we can conclude that adopting a healthy lifestyle is very important in our lives, "
                "having a normal BMI can ensure that our glucose levels are in a normal state, this can be done by controlling how much we consume sugary foods and drinks and how much we practice exercise.</p>", unsafe_allow_html=True)

# Define the page layout for Dashboard 3
def dashboard3():
    st.markdown("<h1 style='text-align: center; margin-bottom: 50px; text-decoration: underline;'>Stroke Analysis by Geographic Distribution</h1>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div>
        <p style='font-size: 21px;text-align: justify;'>
        This dashboard provides a detailed overview of stroke cases in Malaysia's main states, divided into 
        rural and urban areas. The dashboard seeks to give information about the distribution and prevalence 
        of stroke in Malaysia's various regions. This dashboard contains two types of charts which is Clustered 
        Column Chart and Stacked Area Chart. 
        </P>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add a line
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    # Create two columns for the figures and descriptions
    col1, col2 = st.columns([2, 1])
    
    # Display the first figure and its description
    with col1:
        st.write("")
        st.write("")
        st.plotly_chart(fig1)
    with col2:
        st.markdown("")
        st.markdown("<p style='font-size: 21px;text-align: justify;'>Urban residents with private work types have the largest numbers of stroke occurrences when compared to other groups.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 21px;text-align: justify;'>Urban areas frequently have higher levels of air pollution due to reasons such as increasing car traffic and the presence of manufacturers. </p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 21px;text-align: justify;'>Dietary trends in urban areas may differ from those in rural areas, with a larger consumption of processed foods, harmful fats, and a higher intake of sodium.</p>", unsafe_allow_html=True)

    # Display the second figure and its description
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.plotly_chart(fig6)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<p style='font-size: 21px;text-align: justify;'>WP Kuala Lumpur regularly has the greatest number of stroke cases per year when compared to other states.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 21px;text-align: justify;'>The surrounding area's bustling and congested environment generate stress and hence raise the probability of stroke.</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 21px;text-align: justify;'>The high cost of living in WP Kuala Lumpur adds to the financial load, magnifying stress levels among residents and likely contributing to the region's increased stroke incidence.</p>", unsafe_allow_html=True)

    # Add a line
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div>
        <p style='font-size: 21px;text-align: justify;'>
        We may conclude from the information shown in the dashboard that urban regions, particularly WP Kuala 
        Lumpur, have the largest number of stroke incidents when compared to other locations. This can be ascribed to a 
        variety of factors, including rising air pollution, dietary trends, high living costs and stress. These factors 
        combine and lead to the increased total stroke incidence seen in urban areas such as WP Kuala Lumpur.
        </P>
        </div>
        """,
        unsafe_allow_html=True
    )

# Create a select box to switch between dashboards
dashboard_selection = st.sidebar.selectbox('Select Dashboard', ('Stroke Analysis and Risk Factors', 'Health Metrics and Lifestyle Analysis', 'Stroke Analysis by Geographic Distribution'))

# Show the selected dashboard based on the selection
if dashboard_selection == 'Stroke Analysis and Risk Factors':
    dashboard1()
elif dashboard_selection == 'Health Metrics and Lifestyle Analysis':
    dashboard2()
elif dashboard_selection == 'Stroke Analysis by Geographic Distribution':
    dashboard3()
