from database import get_connection
from logger import get_logger
from time import time
from sql_generator import fix_sql

logger = get_logger(__name__)


def executeQuery(sql, question=None, max_retry=1):
    attempt = 0
    current_sql = sql

    logger.info(f"Starting execution | max_retries={max_retry} | question='{question}'")

    while attempt <= max_retry:
        try:
            startTime = time()
            logger.info(f"Attempt {attempt + 1} | SQL:\n{current_sql}")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(current_sql)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            elapsedTime = round(time() - startTime, 2)

            logger.info(f"Attempt {attempt + 1} SUCCESS | Rows returned: {len(results)} | Time: {elapsedTime}s")
            logger.info(f"Columns: {columns}")
            logger.info(f"First row preview: {results[0] if results else 'No rows'}")

            cursor.close()
            conn.close()
            logger.info("Database connection closed")

            return {
                "success": True,
                "sql": current_sql,
                "columns": columns,
                "results": results,
                "rows": len(results),
                "latency": elapsedTime,
                "retries": attempt
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Attempt {attempt + 1} FAILED | Error: {error_msg}")

            if attempt < max_retry:
                logger.warning(f"Retrying... ({attempt + 1}/{max_retry})")
                current_sql = fix_sql(current_sql, error_msg, question)
                attempt += 1
            else:
                logger.error(f"All {max_retry + 1} attempts exhausted — giving up")
                return {
                    "success": False,
                    "sql": current_sql,
                    "error": error_msg,
                    "retries": attempt
                }