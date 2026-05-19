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

model = "llama-3.1-8b-instant"

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
    You are a SQL expert working with the classicmodels PostgreSQL database.
    
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
    You are a SQL expert working with the classicmodels PostgreSQL database.
    IMPORTANT: All mixed-case column names must use double quotes.
    Example: "customerNumber", "orderDate", "productName"
    
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
            model=model,
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
    You are a SQL expert working with the classicmodels PostgreSQL database.
    IMPORTANT: All mixed-case column names must use double quotes.
    Example: "customerNumber", "orderDate", "productName"
        
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
            model=model,
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

def generate_summary(question, sql, result, columns):
    logger.info(f"Generating natural language summary for question: '{question}'")

    # format result nicely for the LLM to read
    if not result:
        result_text = "No rows returned"
    else:
        # build a readable table string
        header = " | ".join(columns)
        rows = "\n".join([" | ".join(str(v) for v in row) for row in result[:10]])
        result_text = f"{header}\n{rows}"

    prompt = f"""
        You are a helpful data analyst.

        The user asked:
        "{question}"

        The SQL query used:
        {sql}

        The query returned this result:
        {result_text}

        Your task:
        Write a clear, natural language response that directly answers the user's question based on the result.

        Guidelines:
        - Be specific and concise
        - Do not mention SQL
        - Do not say phrases like:
        - "based on the query"
        - "the result shows"
        - "the query returned"
        - Answer the question naturally, as if speaking to a business user
        - If the result contains useful trends, comparisons, anomalies, percentages, or patterns, include brief insights
        - If the query failed or no result was produced after multiple attempts:
        - Clearly explain that the data could not be retrieved
        - Mention possible reasons such as missing data, invalid filters, schema mismatch, or execution issues
        - Suggest what the user can check or try next
        - Still provide any partial observations or contextual insights if available
        - Avoid sounding robotic or repetitive
        - Keep the tone professional and informative

        Examples:
        - "Sales increased by 18% in March, with the highest growth coming from the electronics category."
        - "No matching records were found for the selected date range. You may want to verify the filters or check whether data exists for that period."
        - "The request could not be completed after multiple attempts due to inconsistent table mappings. Checking column names or simplifying the filters may help."

        Now generate the response.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        summary = response.choices[0].message.content.strip()
        logger.info(f"Summary generated: {summary}")
        return summary

    except Exception as e:
        logger.error(f"Summary generation failed: {str(e)}")
        return "Could not generate summary."