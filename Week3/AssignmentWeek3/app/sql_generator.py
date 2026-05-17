from dotenv import load_dotenv
import os
from openai import OpenAI
from schema import SCHEMA
from logger import get_logger

load_dotenv()
API_KEY = os.getenv("API_KEY")

logger = get_logger(__name__)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def clean_sql(sql):
    sql = sql.strip()
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]
    cleaned = sql.strip()
    logger.info(f"SQL cleaned | Result: {cleaned}")
    return cleaned


def decompose_question(question):
    logger.info(f"Decomposing question: '{question}'")

    prompt = f"""
    You are a PostgreSQL SQL expert.
    IMPORTANT: All mixed-case column names must use double quotes.
    Example: "customerNumber", "orderDate", "productName"
    
    Database schema:
    {SCHEMA}
    
    Break this question into structured parts:
    Question : "{question}"

    Respond ONLY in this exact format:
    Intent: <what is being asked>
    Tables: <tables needed>
    Columns: <columns needed>
    Filters: <WHERE conditions>
    Joins: <join conditions needed>
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        decomposed_query = response.choices[0].message.content
        logger.info(f"Decomposition successful:\n{decomposed_query}")
        return decomposed_query

    except Exception as e:
        logger.error(f"Decomposition failed: {str(e)}")
        raise


def generateSQL(question, decomposition):
    logger.info(f"Generating SQL for question: '{question}'")

    prompt = f"""
    You are a PostgreSQL SQL expert.
    IMPORTANT: All mixed-case column names must use double quotes.
    Example: "customerNumber", "orderDate", "productName"
    
    Database schema:
    {SCHEMA}
    
    Question: "{question}"
    
    Decomposition:
    {decomposition}
    
    Write a clean, correct PostgreSQL SELECT query for this question.
    Rules:
    - Only SELECT statements allowed
    - No DELETE, DROP, UPDATE, INSERT
    - Use table aliases
    - Return ONLY the SQL query, nothing else
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        sql_query = response.choices[0].message.content
        cleaned = clean_sql(sql_query)
        logger.info(f"SQL generated successfully:\n{cleaned}")
        return cleaned

    except Exception as e:
        logger.error(f"SQL generation failed: {str(e)}")
        raise


def fix_sql(bad_sql, error_msg, question):
    logger.warning(f"Attempting to fix SQL for question: '{question}'")
    logger.warning(f"Failed SQL:\n{bad_sql}")
    logger.warning(f"Error received: {error_msg}")

    prompt = f"""
    You are a PostgreSQL SQL expert.
    IMPORTANT: All mixed-case column names must use double quotes.
    Example: "customerNumber", "orderDate", "productName"
    
    Database schema:
    {SCHEMA}
    
    This SQL query failed with an error. Fix it.
    
    Original question: "{question}"
    
    Failed SQL:
    {bad_sql}
    
    Database error:
    {error_msg}
    
    Return ONLY the corrected SQL query, nothing else.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        sql_query = response.choices[0].message.content
        fixed = clean_sql(sql_query)
        logger.info(f"Fixed SQL:\n{fixed}")
        return fixed

    except Exception as e:
        logger.error(f"SQL fix failed: {str(e)}")
        raise