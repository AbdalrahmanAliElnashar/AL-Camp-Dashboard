import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='AL-CAMP Admins', page_icon=":chart_with_upwards_trend:",layout="wide", 
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
st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:-50px'>AL-CAMP Admins</h1>", unsafe_allow_html=True)
st.divider()

# Top 10 Admins
st.markdown("<h1 style='text-align: center; color: white; font-size: 50px; margin-top:30px;'>TOP Working Admins</h1>", unsafe_allow_html=True)

col4, col5 = st.columns((1,2), gap='medium')
admin_query = '''\
   SELECT
    admins.admin_id,
    COUNT(capstone_evaluation_history.eval_history_id) AS number_of_evaluations
    FROM admins
    LEFT JOIN capstone_evaluation_history ON admins.admin_id = capstone_evaluation_history.admin_id
    GROUP BY admins.admin_id;


    SELECT
        admins.admin_id,
        SUM(CASE WHEN DATE(capstone_evaluation_history.evaluation_date) = CURDATE() THEN 1 ELSE 0 END) AS evaluations_today,
        SUM(CASE WHEN YEARWEEK(capstone_evaluation_history.evaluation_date, 1) = YEARWEEK(CURDATE(), 1) THEN 1 ELSE 0 END) AS evaluations_this_week,
        SUM(CASE WHEN YEAR(capstone_evaluation_history.evaluation_date) = YEAR(CURDATE()) AND MONTH(capstone_evaluation_history.evaluation_date) = MONTH(CURDATE()) THEN 1 ELSE 0 END) AS evaluations_this_month
    FROM admins
    LEFT JOIN capstone_evaluation_history ON admins.admin_id = capstone_evaluation_history.admin_id
    GROUP BY admins.admin_id;

'''

# 3. Read Query
df = pd.read_sql_query(admin_query, conn)
df = df.sort_values('number_of_evaluations', ascending=False)

with col4:
    st.dataframe(df.head(10), column_config={
                "admin_id": st.column_config.NumberColumn('Admin ID', format="🌟 %d",)}, hide_index=True, width=800)
with col5:
    # Create a bar plot with sorted dates
    fig = px.bar(df.sort_values('number_of_evaluations', ascending=False).head(10), x='admin_id', y='number_of_evaluations')
    fig.update_layout(width=1000, height=450)
    fig.update_traces(marker_color='gold')
    st.plotly_chart(fig)
   
st.divider()  


# ----------------------------------------------------------------------------------

# Connect to the MySQL database
conn = mysql.connector.connect(**config)
# Admins Capstones Evaluations

st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:20px'>Admins Capstones Evaluations</h1>", unsafe_allow_html=True)

s = st.selectbox('Interval', ['Today', 'Weekly', 'Monthly'])
query2 = '''\
SELECT
    admins.admin_id,
    SUM(CASE WHEN DATE(capstone_evaluation_history.evaluation_date) = CURDATE() THEN 1 ELSE 0 END) AS evaluations_today,
    SUM(CASE WHEN YEARWEEK(capstone_evaluation_history.evaluation_date, 1) = YEARWEEK(CURDATE(), 1) THEN 1 ELSE 0 END) AS evaluations_this_week,
    SUM(CASE WHEN YEAR(capstone_evaluation_history.evaluation_date) = YEAR(CURDATE()) AND MONTH(capstone_evaluation_history.evaluation_date) = MONTH(CURDATE()) THEN 1 ELSE 0 END) AS evaluations_this_month
	FROM admins
	LEFT JOIN capstone_evaluation_history ON admins.admin_id = capstone_evaluation_history.admin_id
	GROUP BY admins.admin_id;
'''

 # Read Query
df2 = pd.read_sql_query(query2, conn)
col7, col8 = st.columns((1,2), gap='large') 
with col7:
    if s == 'Today':
        df2 = df2.sort_values('evaluations_today', ascending=False)
        st.dataframe(df2[['admin_id', 'evaluations_today']].head(10), column_config={
                        "admin_id": st.column_config.NumberColumn('Admin ID', format="✅ %d",)}, hide_index=True, width=1000)
        
        ex = st.expander('For more Users Completed Courses:', expanded=False )
        ex.dataframe(df2)

        with col8:
            fig = px.bar(df2.head(10), x='admin_id', y='evaluations_today')
            fig.update_layout(width=1000, height=500)
            fig.update_traces(marker_color='gold')
            st.plotly_chart(fig)


    elif s== 'Weekly':
        df2 = df2.sort_values('evaluations_this_week', ascending=False)
        st.dataframe(df2[['admin_id', 'evaluations_this_week']].head(10), column_config={
                        "admin_id": st.column_config.NumberColumn('Admin ID', format="✅ %d",)}, hide_index=True, width=1000)
        
        ex = st.expander('For more Users Completed Courses:', expanded=False )
        ex.dataframe(df2)

        with col8:
            fig = px.bar(df2.head(10), x='admin_id', y='evaluations_this_week')
            fig.update_layout(width=1000, height=500)
            fig.update_traces(marker_color='gold')
            st.plotly_chart(fig)


    elif s== 'Monthly':
        df2 = df2.sort_values('evaluations_this_month', ascending=False)
        st.dataframe(df2[['admin_id', 'evaluations_this_month']].head(10), column_config={
                        "admin_id": st.column_config.NumberColumn('Admin ID', format="✅ %d",)}, hide_index=True, width=1000)
        
        ex = st.expander('For more Users Completed Courses:', expanded=False )
        ex.dataframe(df2)

        with col8:
            fig = px.bar(df2.head(10), x='admin_id', y='evaluations_this_month')
            fig.update_layout(width=1000, height=500)
            fig.update_traces(marker_color='gold')
            st.plotly_chart(fig)


