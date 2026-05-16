from database import get_connection
from logger import get_logger
from time import time

logger = get_logger(__name__)

def executeQuery(sql, question=None, max_retry = 1):
    attempt = 0
    current_sql = sql
    while attempt <= max_retry:
        try:
            startTime = time()
            
            logger.info(f"Attempt {attempt+1} | SQL : {current_sql}")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(current_sql)
            results = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]

            elapsedTime = round(time() - startTime , 2)
            logger.info(f"Success | Rows: {len(results)} | Time: {elapsedTime} s")
            
            cursor.close()
            conn.close()
            
            return {
                "success" : True,
                "sql": current_sql,
                "columns": columns,
                "results" : results,
                "rows": len(results),
                "latency": elapsedTime,
                "retries": attempt
            }
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Attemp {attempt + 1} failed : {error_msg}")

            if attempt < max_retry:
                current_sql = fix_sql(current_sql, error_msg, question)
                attempt += 1
            
            else:
                return {
                    "success" : False,
                    "sql": current_sql,
                    "error": error_msg,
                    "retries": attempt
                }
                

def fix_sql(bad_sql, error_msg, question):
    return bad_sql