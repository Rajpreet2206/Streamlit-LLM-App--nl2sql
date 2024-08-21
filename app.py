from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

## Reading in the env variables
load_dotenv()

## The API-key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Loading the Google-Gemini Model and Providing SQL query
def get_gemini_response(question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

## Retrieving the query form the SQL Database
def read_sql_query(sql, db):
    conn=sqlite3.connect(db)
    cursor=conn.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt=["""
    instruction,output,input
"Please give me the right SQL query based on: 
1. #USER_QUESTION: How many heads of the departments are older than 56 ?
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}",SELECT count(*) FROM head WHERE age  >  56,#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: List the name, born state and age of the heads of departments ordered by age.
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}","SELECT name ,  born_state ,  age FROM head ORDER BY age",#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: List the creation year, name and budget of each department.
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}","SELECT creation ,  name ,  budget_in_billions FROM department",#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: What are the maximum and minimum budget of the departments?
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}","SELECT max(budget_in_billions) ,  min(budget_in_billions) FROM department",#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: What is the average number of employees of the departments whose rank is between 10 and 15?
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}",SELECT avg(num_employees) FROM department WHERE ranking BETWEEN 10 AND 15,#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: What are the names of the heads who are born outside the California state?
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}",SELECT name FROM head WHERE born_state != 'California',#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: What are the distinct creation years of the departments managed by a secretary born in state 'Alabama'?
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}",SELECT DISTINCT T1.creation FROM department AS T1 JOIN management AS T2 ON T1.department_id  =  T2.department_id JOIN head AS T3 ON T2.head_id  =  T3.head_id WHERE T3.born_state  =  'Alabama',#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: What are the names of the states where at least 3 heads were born?
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}",SELECT born_state FROM head GROUP BY born_state HAVING count(*)  >=  3,#SQL_QUERY: 
"Please give me the right SQL query based on: 
1. #USER_QUESTION: In which year were most departments established?
2. # TABLE NAMES and COLUMN NAMES:{'department': ['department id', 'name', 'creation', 'ranking', 'budget in billions', 'num employees'], 'head': ['head id', 'name', 'born state', 'age'], 'management': ['department id', 'head id', 'temporary acting']}",SELECT creation FROM department GROUP BY creation ORDER BY count(*) DESC LIMIT 1,#SQL_QUERY: 

"""]

st.set_page_config(page_title="This GenAI App can generate SQL queries after understanding Natural Language")
st.header("Gemini-Pro App to Retrieve SQL Data")
question=st.text_input("Input: ", key="input")
submit=st.button("Ask the question")

if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response,"LLM_Models.db")
    st.subheader("The response is: ")
    for row in data:
        print(row)
        st.header(row)