import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='10K AI Initiative', page_icon=":chart_with_upwards_trend:",layout="wide", 
                   initial_sidebar_state="expanded")
# 1. Database Connection
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
st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:-50px'>10K AI Initiative</h1>", unsafe_allow_html=True)
st.divider()


col1, col2, col3 = st.columns((1, 2, 1), gap='medium')
with col2:
    st.markdown("<h1 style='text-align: left; font:'bold'; color: gold; font-size: 50px;'>TOP 10 Student in 10K AI Initiative</h1>", unsafe_allow_html=True)
    initiative_query = '''\
       SELECT
        Users.user_id,
        Users.`10k_AI_initiative`,
        COUNT(user_completed_courses.course_id) AS completed_courses_count,
        MAX(user_completed_courses.completion_date) AS last_completion_date,
        (SELECT course_degree
        FROM user_completed_courses AS UC
        WHERE UC.user_id = Users.user_id
        ORDER BY UC.completion_date DESC
        LIMIT 1) AS last_course_degree
        FROM Users
        LEFT JOIN user_completed_courses ON Users.user_id = user_completed_courses.user_id
        WHERE Users.`10k_AI_initiative` = 1
        GROUP BY Users.user_id, Users.`10k_AI_initiative`;
    '''
    df = pd.read_sql_query(initiative_query, conn)
    df = df.sort_values('completed_courses_count', ascending=False)
    #st.dataframe(df.head(10), hide_index=True)

    st.dataframe(df.head(10), column_config={
                "user_id": st.column_config.NumberColumn('USER_ID',format="⭐ %d"),}, hide_index=True, width=1000)
    
    ex = st.expander('For more Users:', expanded=False)
    ex.dataframe(df)

    
    fig = px.bar(df.head(10), x='user_id', y='completed_courses_count')
    fig.update_layout(width=1000, height=450)
    fig.update_traces(marker_color='gold', width=30)
    st.plotly_chart(fig)
