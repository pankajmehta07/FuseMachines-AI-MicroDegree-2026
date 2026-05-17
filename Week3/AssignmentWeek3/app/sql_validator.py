import re
from logger import get_logger

logger = get_logger(__name__)

DANGEROUS_KEYWORDS = [
    "DELETE", "DROP", "UPDATE", "INSERT",
    "TRUNCATE", "ALTER", "CREATE", "EXEC"
]

def validate_sql(sql):
    logger.info(f"Validating SQL:\n{sql}")
    
    sql_upper = sql.upper().strip()

    if not sql_upper.startswith("SELECT"):
        logger.error(f"Validation FAILED — query does not start with SELECT")
        return False, "Query must start with SELECT"

    for keyword in DANGEROUS_KEYWORDS:
        if keyword in sql_upper:
            logger.error(f"Validation FAILED — dangerous keyword detected: {keyword}")
            return False, f"Dangerous keyword detected: {keyword}"

    logger.info("Validation PASSED — query is safe")
    return True, "Valid"