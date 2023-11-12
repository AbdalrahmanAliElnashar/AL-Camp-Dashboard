import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='AI CAMP Users', page_icon=":chart_with_upwards_trend:",layout="wide", 
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
st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:-50px;'>AL-CAMP USERs</h1>", unsafe_allow_html=True)
st.divider()


# ----------------------------------------------------------------------------------

col1, col2, col3 = st.columns((1, 1, 2), gap='large')
with col1:
    st.markdown("<h1 style='text-align: left; font:'bold'; color: white; font-size: 60px;'>TOP 10 Active Users</h1>", unsafe_allow_html=True)
    st.text('TOP Users Currently Learning Courses')
    curr_courses_query = '''\
        SELECT
        Users.user_id,
        COUNT(user_courses.course_id) AS currently_learning_courses_count
        FROM Users
        LEFT JOIN user_courses ON Users.user_id = user_courses.user_id
        GROUP BY Users.user_id;
    '''
    df = pd.read_sql_query(curr_courses_query, conn)
    df = df.sort_values('currently_learning_courses_count', ascending=False)
    #st.dataframe(df.head(10), hide_index=True)

    st.dataframe(df.head(10), column_config={
                "user_id": st.column_config.NumberColumn('USER_ID',format="⭐ %d"),
                "currently_learning_courses_count": "Currently Learning Courses Count"}, hide_index=True, width=500)
    
    ex = st.expander('For more Users:', expanded=False)
    ex.dataframe(df)

with col2:
    st.markdown("<h1 style='text-align: left; font:'bold'; color: white; font-size: 60px;'>TOP 10 Serious Users</h1>", unsafe_allow_html=True)
    st.text('TOP Users Completed Learning Courses')
    comp_courses_query = '''\
        SELECT
    Users.user_id,
    COUNT(user_completed_courses.course_id) AS completed_courses_count
    FROM Users
    LEFT JOIN user_completed_courses ON Users.user_id = user_completed_courses.user_id
    GROUP BY Users.user_id;
    '''
    df = pd.read_sql_query(comp_courses_query, conn)
    df = df.sort_values('completed_courses_count', ascending=False)
    #st.dataframe(df.head(10), hide_index=True)

    st.dataframe(df.head(10), column_config={
                "user_id": st.column_config.NumberColumn('USER_ID', format="⭐ %d",),
                "completed_courses_count": "Completed Courses Count"}, hide_index=True, width=500)
    
    ex = st.expander('For more Users:', expanded=False )
    ex.dataframe(df)


with col3:
    st.markdown("<h1 style='text-align: left; font:'bold'; color: red; font-size: 60px;'>Users Uncompleted Courses</h1>", unsafe_allow_html=True)
    st.text('Users Uncompleted Courses Count')
    diff_query = '''\
        SELECT
    Users.user_id,
    COUNT(DISTINCT user_courses.course_id) AS currently_learning_courses_count,
    COUNT(DISTINCT user_completed_courses.course_id) AS completed_courses_count,
    (COUNT(DISTINCT user_courses.course_id) - COUNT(DISTINCT user_completed_courses.course_id)) AS uncompleted_courses 
    
    FROM Users
    LEFT JOIN user_courses ON Users.user_id = user_courses.user_id
    LEFT JOIN user_completed_courses ON Users.user_id = user_completed_courses.user_id
    GROUP BY Users.user_id;
    '''

    df = pd.read_sql_query(diff_query, conn)
    df = df.sort_values('currently_learning_courses_count', ascending=False)

    st.dataframe(df.head(10), column_config={
                "user_id": st.column_config.NumberColumn('USER_ID', format="⭐ %d",)}, hide_index=True, width=1000)
    
    ex = st.expander('For more Users:', expanded=False )
    ex.dataframe(df)
st.divider()

# All Users Completed Courses
st.markdown("<h1 style='text-align: center; color: white; font-size: 50px; margin-top:30px;'>User Completed Courses</h1>", unsafe_allow_html=True)
s = st.selectbox('Interval', ['Weekly', 'Monthly', 'Yearly'])
query3 = '''\
SELECT
    Users.user_id,
    SUM(CASE WHEN DATEDIFF(NOW(), user_completed_courses.completion_date) <= 7 THEN 1 ELSE 0 END) AS completed_courses_by_week,
    SUM(CASE WHEN YEAR(user_completed_courses.completion_date) = YEAR(NOW()) THEN 1 ELSE 0 END) AS completed_courses_year,
    SUM(CASE WHEN YEAR(user_completed_courses.completion_date) = YEAR(NOW()) AND MONTH(user_completed_courses.completion_date) = MONTH(NOW()) THEN 1 ELSE 0 END) AS completed_courses_month
    FROM Users
    LEFT JOIN user_completed_courses ON Users.user_id = user_completed_courses.user_id
    GROUP BY Users.user_id;
'''

 # Read Query
df3 = pd.read_sql_query(query3, conn)
col7, col8 = st.columns((1,2), gap='large') 

with col7:
    if s == 'Weekly':
        df3 = df3.sort_values('completed_courses_by_week', ascending=False)
        st.dataframe(df3[['user_id', 'completed_courses_by_week']].head(10), column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=1000)
        ex = st.expander('For more Users Completed Courses:', expanded=False )
        ex.dataframe(df3)

        with col8:
            fig = px.bar(df3.head(10), x='user_id', y='completed_courses_by_week')
            fig.update_layout(width=1000, height=500)
            fig.update_traces(marker_color='gold', width=25)
            st.plotly_chart(fig)

    elif s== 'Monthly':
        df3 = df3.sort_values('completed_courses_month', ascending=False)
        st.dataframe(df3[['user_id', 'completed_courses_month']].head(10), column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=1000)
        ex = st.expander('For more Users Completed Courses:', expanded=False )
        ex.dataframe(df3)

        with col8:
            fig = px.bar(df3.head(10), x='user_id', y='completed_courses_month')
            fig.update_layout(width=1000, height=500)
            fig.update_traces(marker_color='gold', width=25)
            st.plotly_chart(fig)

    elif s== 'Yearly':
        df3 = df3.sort_values('completed_courses_year', ascending=False)
        st.dataframe(df3[['user_id', 'completed_courses_year']].head(10), column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=1000)
        ex = st.expander('For more Users Completed Courses:', expanded=False )
        ex.dataframe(df3)

        with col8:
            fig = px.bar(df3.head(10), x='user_id', y='completed_courses_year')
            fig.update_layout(width=1000, height=500)
            fig.update_traces(marker_color='gold', width=25)
            st.plotly_chart(fig)

st.divider()

# -----------------------------------------------------------------------------------------


# Uncompleted Courses
st.markdown("<h1 style='text-align: center; color: white; font-size: 50px; margin-top:30px;'>Most Users Uncompleted Courses</h1>", unsafe_allow_html=True)

col4, col5 = st.columns((1,2), gap='large')    


df = df.sort_values('uncompleted_courses', ascending=False)

with col4:
    st.dataframe(df[['user_id', 'uncompleted_courses']].head(10), column_config={
                "user_id": st.column_config.NumberColumn('USER_ID', format="⚠️ %d",)}, hide_index=True, width=800)
with col5:
    # Create a bar plot with sorted dates
    fig = px.bar(df.sort_values('uncompleted_courses', ascending=False).head(10), x='user_id', y='uncompleted_courses',category_orders={'uncompleted_courses': sorted(df['uncompleted_courses'])})
    fig.update_layout(width=1000, height=450)
    fig.update_traces(marker_color='gold')
    st.plotly_chart(fig)

        



