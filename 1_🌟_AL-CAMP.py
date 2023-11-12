import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(page_title='AI CAMP DASHBOARD', page_icon=":chart_with_upwards_trend:",layout="wide", 
                   initial_sidebar_state="expanded", )


# Database Connection
config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'test'
}

# Connect to the MySQL database
conn = mysql.connector.connect(**config)

# ----------------------------------------------------------------------------------

# Title
st.markdown("<h1 style='text-align: center; color: white; font-size: 50px; margin-top:-50px;'>AL-CAMP Insights</h1>", unsafe_allow_html=True)
st.divider()

# Sidebar

# ----------------------------------------------------------------------------------

# Dashboard1
s = st.selectbox('Interval', ['Daily', 'Weekly', 'Monthly', 'Yearly'])
col1, col2 = st.columns(2, gap='large')

with col1:
    st.markdown("<h2 style='text-align: center; font:'bold'; color: white; font-size: 40px;'>Registered Users</h2>", unsafe_allow_html=True)
with col2:
    st.markdown("<h2 style='text-align: center; color: white; font:'bold'; font-size: 40px;'>Subscribed Users</h2>", unsafe_allow_html=True)



# Daily Query
daily_query = '''\
    SELECT 
        DATE(registration_date) AS date,
        COUNT(*) AS registusersered_users,
        SUM(CASE WHEN subscription_date IS NOT NULL THEN 1 ELSE 0 END) AS subscribed_users
    FROM users
    GROUP BY DATE(registration_date)
    ORDER BY date;

'''
daily_data = pd.read_sql_query(daily_query, conn)

if s =='Daily':
    with col1:
        fig = px.line(daily_data, x='date',  y='registusersered_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Registerd Users per Day', xaxis_title='Date by Day', yaxis_title='Registerd Users')
        fig.update_traces(line=dict(color='red', width=3, dash='dot'))
        st.plotly_chart(fig)
    with col2:
        fig = px.line(daily_data, x='date',  y='subscribed_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Subscribed Users per Day', xaxis_title='Date by Date', yaxis_title='Subscribed Users')
        fig.update_traces(line=dict(color='blue', width=3, dash='dot'))
        st.plotly_chart(fig)



# Weekly Query
weekly_query = '''\
    SELECT 
    WEEK(registration_date) AS week,
    COUNT(*) AS registered_users,
    SUM(CASE WHEN subscription_date IS NOT NULL THEN 1 ELSE 0 END) AS subscribed_users
FROM users
GROUP BY WEEK(registration_date)
ORDER BY week;

'''
weekly_data = pd.read_sql_query(weekly_query, conn)

if s =='Weekly':
    with col1:
        fig = px.line(weekly_data, x='week',  y='registered_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Registerd Users per Week', xaxis_title='Date by week', yaxis_title='Registerd Users')
        fig.update_traces(line=dict(color='red', width=3, dash='dot'))
        st.plotly_chart(fig)
    with col2:
        fig = px.line(weekly_data, x='week',  y='subscribed_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Subscribed Users per Week', xaxis_title='Date by week', yaxis_title='Subscribed Users')
        fig.update_traces(line=dict(color='blue', width=3, dash='dot'))
        st.plotly_chart(fig)


# Monthly Query
monthly_query = '''\
    SELECT 
    YEAR(registration_date) AS year,
    MONTH(registration_date) AS month,
    COUNT(*) AS registered_users,
    SUM(CASE WHEN subscription_date IS NOT NULL THEN 1 ELSE 0 END) AS subscribed_users
    FROM users
    GROUP BY YEAR(registration_date), MONTH(registration_date)
    ORDER BY year, month;

'''
montly_data = pd.read_sql_query(monthly_query, conn)

if s =='Monthly':
    with col1:
        fig = px.line(montly_data, x='month',  y='registered_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Registerd Users per Month', xaxis_title='Date by Month', yaxis_title='Registerd Users')
        fig.update_traces(line=dict(color='red', width=3, dash='dot'))
        st.plotly_chart(fig)
    with col2:
        fig = px.line(montly_data, x='month',  y='subscribed_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Subscribed Users per Month', xaxis_title='Date by Month', yaxis_title='Subscribed Users')
        fig.update_traces(line=dict(color='blue', width=3, dash='dot'))
        st.plotly_chart(fig)


# Monthly Query
yearly_query = '''\
    SELECT 
    YEAR(registration_date) AS year,
    COUNT(*) AS registered_users,
    SUM(CASE WHEN subscription_date IS NOT NULL THEN 1 ELSE 0 END) AS subscribed_users
    FROM users
    GROUP BY year
    ORDER BY year;

'''
yearly_data = pd.read_sql_query(yearly_query, conn)

if s =='Yearly':
    with col1:
        fig = px.line(yearly_data, x='year',  y='registered_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Registerd Users per Year', xaxis_title='Date by Year', yaxis_title='Registerd Users')
        fig.update_traces(line=dict(color='red', width=3, dash='dot'))
        st.plotly_chart(fig)
    with col2:
        fig = px.line(yearly_data, x='year',  y='subscribed_users', markers=True)
        fig.update_layout(width=800, height=500, title='Number of Subscribed Users per Year', xaxis_title='Date by Year', yaxis_title='Subscribed Users')
        fig.update_traces(line=dict(color='blue', width=3, dash='dot'))
        st.plotly_chart(fig)    




# ----------------------------------------------------------------------------------

# Dashboard 9
# Users Statistics [Ages , Degress, Gender]
#st.markdown("<h1 style='text-align: center; color: white; font-size: 50px; margin-top:30px;'>Users Statistics</h1>", unsafe_allow_html=True)
st.divider()

col3, col4, col5 = st.columns(3, gap='large')

with col3:
    st.markdown("<h2 style='text-align: center; font:'bold'; color: white; font-size: 40px;'>Users Study Degress</h2>", unsafe_allow_html=True)
    degree_query = '''\
        SELECT
            study_degree,
            COUNT(*) AS user_count
        FROM users
        GROUP BY study_degree;
    '''
    degree_data = pd.read_sql_query(degree_query, conn)
    fig = px.pie(degree_data, values='user_count', names='study_degree',
                  color_discrete_sequence=['blue', 'red'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(width=700, height=600)
    st.plotly_chart(fig)


with col4:
    st.markdown("<h2 style='text-align: center; font:'bold'; color: white; font-size: 40px;'>Users Ages</h2>", unsafe_allow_html=True)
    age_query = '''\
       SELECT
        age,
        COUNT(*) AS user_count
        FROM users
        GROUP BY age;;
    '''
    age_data = pd.read_sql_query(age_query, conn)
    fig = px.bar(age_data, x='age', y='user_count', color='user_count', color_continuous_scale='Bluered_r')
    fig.update_layout(width=700, height=600)
    st.plotly_chart(fig)


with col5:
    st.markdown("<h2 style='text-align: center; font:'bold'; color: white; font-size: 40px;'>Users Gender</h2>", unsafe_allow_html=True)
    gender_query = '''\
        SELECT
            gender,
            COUNT(*) AS user_count
        FROM users
        GROUP BY gender;
    '''
    gender_data = pd.read_sql_query(gender_query, conn)
    fig = px.pie(gender_data, values='user_count', names={'m':'Male', 'f': 'Female'},
                  color_discrete_sequence=['red', 'blue'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(width=700, height=600)
    st.plotly_chart(fig)
 