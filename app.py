# Import Libraries
import sqlite3
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("🔑 Google API Key not found. Please check your environment variables.")
    st.stop()

genai.configure(api_key=api_key)

# Function to load Google Gemini Model and provide query as response
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        combined_prompt = f"{prompt}\nQuestion: {question}"
        response = model.generate_content(combined_prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"⚠️ Error getting response from Gemini API: {e}")
        return None

# Function to retrieve query from SQL Database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [description[0] for description in cur.description]
        conn.close()

        # Format rows into a string
        result = "\n".join([", ".join(map(str, row)) for row in rows])
        return result
    except sqlite3.Error as e:
        st.error(f"⚠️ SQL error: {e}")
        return None

# Define the Prompt
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, MARKS.

For example,
Example 1 - How many entries of records are present?, 
the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
Example 2 - Tell me all the students studying in Data Science class?, 
the SQL command will be something like this: SELECT * FROM STUDENT where CLASS="Data Science";
also the SQL code should not have ``` in the beginning or end and the SQL word in output.
"""

# Setup Streamlit Application
st.set_page_config(page_title="📝 SQL Query Converter: Effortless Database Exploration")
st.title("🔍 SQL Query Converter: Effortless Database Exploration")

# Center alignment style
centered_heading = """
    <style>
    .centered-heading {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;  /* Green color */
        margin-top: 20px;
    }
    .centered-response {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        font-size: 18px;
        color: #FF5722;  /* Orange color */
        margin-top: 10px;
    }
    .data-table {
        margin-left: auto;
        margin-right: auto;
        margin-top: 10px;
    }
    .stButton>button {
        background-color: #2196F3; /* Blue color */
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
    }
    </style>
"""

st.markdown(centered_heading, unsafe_allow_html=True)

question = st.text_input("💬 Enter Your Query:", key="input")
submit = st.button("🚀 Ask the Question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    
    if response:
        st.markdown(f'<div class="centered-heading">📋 Generated SQL Query:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="centered-response">{response}</div>', unsafe_allow_html=True)
        
        if response.lower().startswith("select"):
            result = read_sql_query(response, "student.db")
            st.markdown(f'<div class="centered-heading">📊 The Response is:</div>', unsafe_allow_html=True)
            if result:
                st.markdown(f'<div class="centered-response">{result}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="centered-response">🔍 No data found for the generated query.</div>', unsafe_allow_html=True)
        else:
            st.error("⚠️ The generated response is not a valid SQL query.")
    else:
        st.error("⚠️ Failed to generate SQL query from the provided question.")
