from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logger import get_logger
from sql_generator import decompose_question, generateSQL, generate_summary
from sql_validator import validate_sql
from sql_executor import executeQuery
from time import time

logger = get_logger(__name__)

app = FastAPI(
    title="Text-to-SQL Agent",
    description="An agentic system that converts natural language to SQL",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    sql: str
    result: object
    summary: str
    status: str


@app.get("/")
def root():
    return {"message": "Text-to-SQL Agent is running"}


@app.post("/agent/sql", response_model=AgentResponse)
def agent_sql(request: QuestionRequest):

    question = request.question
    pipeline_start = time()

    logger.info("=" * 60)
    logger.info(f"AGENT REQUEST | Question: '{question}'")
    logger.info("=" * 60)

    logger.info("STEP 1 — Understanding query (decomposition)")
    step1_start = time()

    try:
        decomposition = decompose_question(question)
        step1_time = round(time() - step1_start, 3)
        logger.info(f"Decomposition completed in {step1_time}s:\n{decomposition}")
    except Exception as e:
        logger.error(f"Decomposition failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to understand question: {str(e)}"
        )

    logger.info("STEP 2 — Generating SQL")
    step2_start = time()

    try:
        sql = generateSQL(question, decomposition)
        step2_time = round(time() - step2_start, 3)
        logger.info(f"SQL generated in {step2_time}s:\n{sql}")
    except Exception as e:
        logger.error(f"SQL generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate SQL: {str(e)}"
        )

    logger.info("STEP 3 — Validating SQL")

    is_valid, reason = validate_sql(sql)
    if not is_valid:
        logger.error(f"SQL validation failed: {reason}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid SQL generated: {reason}"
        )
    logger.info("SQL validation passed")

    logger.info("STEP 4 — Executing SQL (max 3 retries)")
    step4_start = time()

    result = executeQuery(sql, question, max_retry=3)
    step4_time = round(time() - step4_start, 3)
    logger.info(f"Execution completed in {step4_time}s")

    if not result["success"]:
        logger.error(f"All retries exhausted | error: {result['error']}")
        return AgentResponse(
            sql=result["sql"],
            result=None,
            summary="The query could not be executed after multiple attempts.",
            status="failed"
        )

    logger.info("STEP 5 — Generating natural language summary")

    summary = generate_summary(
        question,
        result["sql"],
        result["results"],
        result["columns"]
    )
    raw_results = result["results"]
    if len(raw_results) == 1 and len(raw_results[0]) == 1:
        formatted_result = raw_results[0][0]
    else:
        formatted_result = [
            dict(zip(result["columns"], row))
            for row in raw_results[:10] 
        ]

    total_time = round(time() - pipeline_start, 3)

    logger.info(f"AGENT SUCCESS | total_time={total_time}s | retries={result['retries']}")
    logger.info("=" * 60)

    return AgentResponse(
        sql=result["sql"],
        result=formatted_result,
        summary=summary,
        status="success"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="0.0.0.0", port=8001, reload=True)