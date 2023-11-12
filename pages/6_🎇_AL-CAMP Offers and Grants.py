import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='AL-CAMP Offers and Grants', page_icon=":chart_with_upwards_trend:",layout="wide", 
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
st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:-50px'>AL-CAMP Offers and Grants</h1>", unsafe_allow_html=True)
st.divider()

st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:20px'>Employment Grant</h1>", unsafe_allow_html=True)
s = st.selectbox('Users Employment Grant Status', ['Submitted', 'Pending', 'Hold', 'Inreview', 'Shortlist', 'Postponed','Accepted'])

if s == 'Submitted':
    sub_query = '''\
    SELECT
    user_id,
    submitted
    FROM Users_employment_grant_actions
    WHERE submitted IS NOT NULL;
    '''
    df = pd.read_sql_query(sub_query, conn)
    sub_count = df['user_id'].count()
    col6, col7, col8 = st.columns((1, 2, 1), gap='large') 
    with col7:
        st.header(f'Total Number of Submitted Users: {sub_count}')
        st.dataframe(df, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=800)
        

elif s == 'Pending':
    pen_query = '''\
    SELECT
    user_id,
    pending
    FROM Users_employment_grant_actions
    WHERE pending IS NOT NULL;
    '''
    df = pd.read_sql_query(pen_query, conn)
    pen_count = df['user_id'].count()
    col6, col7, col8 = st.columns((1, 2, 1), gap='large') 
    with col7:
        st.header(f'Total Number of Pending Users: {pen_count}')
        st.dataframe(df, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=800)

elif s == 'Hold':
    hold_query = '''\
    SELECT
    user_id,
    hold
    FROM Users_employment_grant_actions
    WHERE hold IS NOT NULL;
    '''
    df = pd.read_sql_query(hold_query, conn)
    hold_count = df['user_id'].count()
    col6, col7, col8 = st.columns((1, 2, 1), gap='large') 
    with col7:
        st.header(f'Total Number of Hold Users: {hold_count}')
        st.dataframe(df, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=800)

elif s == 'Inreview':
    inter_query = '''\
    SELECT
    user_id,
    inreview
    FROM Users_employment_grant_actions
    WHERE inreview IS NOT NULL;
    '''
    df = pd.read_sql_query(inter_query, conn)
    inter_count = df['user_id'].count()
    col6, col7, col8 = st.columns((1, 2, 1), gap='large') 
    with col7:
        st.header(f'Total Number of Inreview Users: {inter_count}')
        st.dataframe(df, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=800)

elif s == 'Shortlist':
    short_query = '''\
    SELECT
    user_id,
    shortlisted
    FROM Users_employment_grant_actions
    WHERE shortlisted IS NOT NULL;
    '''
    df = pd.read_sql_query(short_query, conn)
    short_count = df['user_id'].count()
    col6, col7, col8 = st.columns((1, 2, 1), gap='large') 
    with col7:
        st.header(f'Total Number of Shortlisted Users: {short_count}')
        st.dataframe(df, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=800)

elif s == 'Postponed':
    post_query = '''\
    SELECT
    user_id,
    postponed
    FROM Users_employment_grant_actions
    WHERE postponed IS NOT NULL;
    '''
    df = pd.read_sql_query(post_query, conn)
    post_count = df['user_id'].count()
    col6, col7, col8 = st.columns((1, 2, 1), gap='large') 
    with col7:
        st.header(f'Total Number of Postponed Users: {post_count}')
        st.dataframe(df, column_config={    
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=800)

elif s == 'Accepted':
    ac_query = '''\
    SELECT
    user_id,
    accepted
    FROM Users_employment_grant_actions
    WHERE accepted IS NOT NULL;
    '''
    df = pd.read_sql_query(ac_query, conn)
    ac_count = df['user_id'].count()
    col6, col7, col8 = st.columns((1, 2, 1), gap='large') 
    with col7:
        st.header(f'Total Number of Accepted Users: {ac_count}')
        st.dataframe(df, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=800)

st.divider()




# ----------------------------------------------------------
col1, col2 = st.columns(2, gap='large')

with col1:
    # Mostly Used Coupons
    st.markdown("<h1 style='text-align: center; color: white; font-size: 50px; margin-top:30px;'>Mostly Used Coupons</h1>", unsafe_allow_html=True)
    copon_query = '''\
    SELECT
        C.coupon_id,
        C.copon_code,
        C.exp_date,
        COUNT(U.user_id) AS actual_users_count
        FROM copons C
        LEFT JOIN users U ON FIND_IN_SET(C.copon_code, U.coupon)
        GROUP BY C.coupon_id, C.copon_code, C.exp_date;

    '''

    # 3. Read Query
    df = pd.read_sql_query(copon_query, conn)
    df = df.sort_values('actual_users_count', ascending=False)
    # Create a bar plot with sorted dates
    fig = px.bar(df.sort_values('actual_users_count', ascending=False).head(10), x='copon_code', y='actual_users_count')
    fig.update_layout(width=800, height=600)
    fig.update_traces(marker_color='gold')
    st.plotly_chart(fig)
with col2:
    st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:20px'>Most Used Bundles</h1>", unsafe_allow_html=True)

    s = st.selectbox('Interval', ['Today', 'Weekly', 'Monthly', 'Yearly'])
    query2 = '''\
    SELECT
        bundle_name,
        DATE(creation_date) AS daily,
        WEEK(creation_date) AS weekly,
        MONTH(creation_date) AS monthly,
        YEAR(creation_date) AS yearly,
        COUNT(DISTINCT user_id) AS subscribed_users
        FROM bundles
        GROUP BY bundle_name, daily, weekly, monthly, yearly
        ORDER BY bundle_name, daily;
    '''

    # Read Query
    df2 = pd.read_sql_query(query2, conn)
    if s == 'Today':
        # Create a bar plot with sorted dates
        fig = px.bar(df2.sort_values('subscribed_users', ascending=True).head(10), x='daily', y='subscribed_users' ,color='bundle_name'
                     , color_discrete_sequence=['red', 'blue', 'gold'], barmode='group')
        fig.update_layout(width=800, height=500)
        fig.update_traces()
        st.plotly_chart(fig)

    if s == 'Weekly':
        # Create a bar plot with sorted dates
        fig = px.bar(df2.sort_values('subscribed_users', ascending=True).head(10), x='weekly', y='subscribed_users' ,color='bundle_name'
                     ,color_discrete_sequence=['red', 'blue', 'gold'], barmode='group')
        fig.update_layout(width=800, height=500)
        fig.update_traces()
        st.plotly_chart(fig)

    if s == 'Monthly':
        # Create a bar plot with sorted dates
        fig = px.bar(df2.sort_values('subscribed_users', ascending=True).head(10), x='monthly', y='subscribed_users' ,color='bundle_name'
                     ,color_discrete_sequence=['red', 'blue', 'gold'], barmode='group')
        fig.update_layout(width=800, height=500)
        fig.update_traces()
        st.plotly_chart(fig)

    if s == 'Yearly':
        # Create a bar plot with sorted dates
        fig = px.bar(df2.sort_values('subscribed_users', ascending=True).head(10), x='yearly', y='subscribed_users' ,color='bundle_name'
                     ,color_discrete_sequence=['red', 'blue', 'gold'],barmode='group')
        fig.update_layout(width=800, height=500)
        fig.update_traces()
        st.plotly_chart(fig)
    
   

    




    
