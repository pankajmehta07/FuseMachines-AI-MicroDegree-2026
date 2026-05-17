from logger import get_logger
from sql_executor import executeQuery
from sql_generator import generateSQL, decompose_question
from sql_validator import validate_sql
import json

logger = get_logger(__name__)


def run_pipeline(question):
    logger.info("=" * 60)
    logger.info(f"PIPELINE START | Question: '{question}'")
    logger.info("=" * 60)

    print(f"\n🔍 Question: {question}")

    # Step 1 — Decompose
    logger.info("STEP 1 — Decomposing question")
    decomposition = decompose_question(question)
    print(f"📋 Decomposition:\n{decomposition}")

    # Step 2 — Generate SQL
    logger.info("STEP 2 — Generating SQL")
    sql = generateSQL(question, decomposition)
    print(f"⚙️  Generated SQL:\n{sql}")

    # Step 3 — Validate
    logger.info("STEP 3 — Validating SQL")
    is_valid, reason = validate_sql(sql)
    if not is_valid:
        logger.error(f"Pipeline stopped — invalid SQL: {reason}")
        return {"status": "error", "reason": reason}
    print("✅ SQL is valid")

    # Step 4 — Execute
    logger.info("STEP 4 — Executing SQL")
    result = executeQuery(sql, question, max_retry=1)

    # Step 5 — Build output
    logger.info("STEP 5 — Building output")
    if result["success"]:
        output = {
            "question": question,
            "sql": result["sql"],
            "columns": result["columns"],
            "result": result["results"][:5],
            "total_rows": result["rows"],
            "latency_seconds": result["latency"],
            "retries": result["retries"],
            "status": "success"
        }
        logger.info(f"PIPELINE SUCCESS | rows={result['rows']} | retries={result['retries']} | latency={result['latency']}s")
    else:
        output = {
            "question": question,
            "sql": result["sql"],
            "error": result["error"],
            "status": "failed"
        }
        logger.error(f"PIPELINE FAILED | error={result['error']}")

    logger.info("=" * 60)
    logger.info("PIPELINE END")
    logger.info("=" * 60)

    print(json.dumps(output, indent=2, default=str))
    return output


if __name__ == "__main__":
    run_pipeline("Show all orders placed by customers in Germany")
    run_pipeline("How many customers are from the USA?")
    run_pipeline("What are the top 5 products by total revenue?")