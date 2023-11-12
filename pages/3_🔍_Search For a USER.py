import streamlit as st
import pandas as pd
import mysql.connector
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title='AI CAMP Search', page_icon=":chart_with_upwards_trend:",layout="wide", 
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
st.markdown("<h1 style='text-align: center; underline:true; color: white; font-size: 50px; margin-top:-50px;'> 🔍 Search For a User!</h1>", unsafe_allow_html=True)
st.divider()
user_id = st.number_input('Enter User ID', min_value=1, max_value=100000, value=1, step=1, format="%d", key=None)

# ----------------------------------------------------------------------------------

# User Information
info_query = f'''
-- Select all information about a specific user, number of completed courses, and number of currently learning courses
SELECT
    U.user_id,
    U.subscribed,
    U.subscription_date,
    U.coupon,
    U.study_degree,
    U.level,
    U.gender,
    U.age,
    U.10k_AI_initiative,
    B.bundle_name,
    EG.status as employment_grant_status,
    COUNT(DISTINCT UCC.course_id) AS completed_courses_count,
    COUNT(DISTINCT UC.course_id) AS currently_learning_courses_count
FROM Users U
LEFT JOIN user_completed_courses UCC ON U.user_id = UCC.user_id
LEFT JOIN user_courses UC ON U.user_id = UC.user_id
LEFT JOIN bundles B ON U.user_id = B.user_id
LEFT JOIN users_employment_grant EG ON U.user_id = EG.user_id

WHERE U.user_id = {user_id}
GROUP BY
    U.user_id,
    U.subscribed,
    U.subscription_date,
    U.coupon,
    U.study_degree,
    U.level,
    U.gender,
    U.age,
    U.10k_AI_initiative,
    B.bundle_name,
    EG.status;

'''

info_data = pd.read_sql_query(info_query, conn)

st.markdown("<h2 style='text-align: center; font:'bold'; color: white; font-size: 60px; margin-top:30px;'>User Information</h2>", unsafe_allow_html=True)
if info_data.empty:
    st.warning('No User Found!')
else:
    #expander = st.expander('User Information')
    #expander.dataframe(info_data, width=800)
    st.dataframe(info_data, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ",)}, hide_index=True, width=2000)



# ----------------------------------------------------------------------------------
# User Capstones Evaluatin History
capstone_query = f'''
-- Select capstone evaluation history for a specific user
SELECT
    eval_history_id,
    user_id,
    admin_id,
    course_id,
    chapter_id,
    lesson_id,
    degree,
    evaluation_date
FROM Capstone_evaluation_history
WHERE user_id = {user_id};
'''

capstone_data = pd.read_sql_query(capstone_query, conn)
if info_data.empty:
    st.warning('No User Found!')
else:
    #expander = st.expander('User Capstones Evaluation History')
    #expander.dataframe(capstone_data, width=800)
    #st.dataframe(capstone_data, width=800)
    col6, col7, col8 = st.columns((1, 2, 1), gap='medium') 
    with col7:
        st.markdown("<h2 style='text-align: center; font:'bold'; color: white; font-size: 60px; margin-top:30px;'>User Capstones Evaluation History</h2>", unsafe_allow_html=True)
        st.dataframe(capstone_data, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=1000)


# ----------------------------------------------------------------------------------
# User Quizzes and Capstonse [User Lesson History Table]
quiz_query = f'''
-- User Quizzes and Capstones
-- Replace 'your_user_id' with the actual user_id you are interested in
-- Select all columns for a specific user with degree greater than 50
SELECT
    user_id,
    course_id,
    chapter_id,
    lesson_id,
    degree,
    last_viewed
FROM User_lesson_history
WHERE user_id = {user_id}
    AND degree > 50;
'''

quiz_data = pd.read_sql_query(quiz_query, conn)
if info_data.empty:
    st.warning('No User Found!')
else:
    #expander = st.expander('User Quizzes and Capstones')
    #expander.dataframe(info_data, width=800)
    #st.dataframe(quiz_data, width=800)
    st.markdown("<h2 style='text-align: center; font:'bold'; color: white; font-size: 60px; margin-top:30px;'>User Completed Quizzes and Capstones</h2>", unsafe_allow_html=True)
    col6, col7, col8 = st.columns((1, 2, 1), gap='medium') 
    with col7:
        st.dataframe(quiz_data, column_config={
                    "user_id": st.column_config.NumberColumn('USER_ID', format="%d ✅",)}, hide_index=True, width=1000)
        

    







