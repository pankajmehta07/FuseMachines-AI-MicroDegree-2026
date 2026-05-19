from logger import get_logger
from sql_executor import executeQuery
from sql_generator import generateSQL, decompose_question
from sql_validator import validate_sql
import json
import csv

logger = get_logger(__name__)


def run_pipeline(question, max_retry=1):
    logger.info("=" * 60)
    logger.info(f"PIPELINE START | Question: '{question}'")
    logger.info("=" * 60)

    print(f"\n🔍 Question: {question}")

    logger.info("STEP 1 — Decomposing question")
    decomposition = decompose_question(question)
    print(f"📋 Decomposition:\n{decomposition}")

    logger.info("STEP 2 — Generating SQL")
    sql = generateSQL(question, decomposition)
    print(f"⚙️  Generated SQL:\n{sql}")

    logger.info("STEP 3 — Validating SQL")
    is_valid, reason = validate_sql(sql)

    if not is_valid:
        logger.error(f"Pipeline stopped — invalid SQL: {reason}")
        return {
            "question": question,
            "status": "error",
            "reason": reason
        }

    print("✅ SQL is valid")

    logger.info("STEP 4 — Executing SQL")
    result = executeQuery(sql, question, max_retry=max_retry)

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

        logger.info(
            f"PIPELINE SUCCESS | rows={result['rows']} | "
            f"retries={result['retries']} | latency={result['latency']}s"
        )

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


def load_questions(csv_path):
    questions = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if row:
                questions.append(row[0].strip())

    return questions

if __name__ == "__main__":


    csv_file = "sql/sql_questions_only.csv"

    questions = load_questions(csv_file)

    logger.info(f"Loaded {len(questions)} questions from CSV")

    all_outputs = []

    for idx, question in enumerate(questions, start=1):
        print(f"\n{'#' * 70}")
        print(f"RUNNING QUESTION {idx}/{len(questions)}")
        print(f"{'#' * 70}")

        try:
            output = run_pipeline(question)
            all_outputs.append(output)

        except Exception as e:
            logger.exception(f"Unexpected error while processing question: {question}")

            all_outputs.append({
                "question": question,
                "status": "crashed",
                "error": str(e)
            })

    with open("logs/pipeline_results.json", "w", encoding="utf-8") as f:
        json.dump(all_outputs, f, indent=2, default=str)

    print("\n✅ Finished processing all questions")
