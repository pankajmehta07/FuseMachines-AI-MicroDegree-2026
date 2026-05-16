# from fastapi import FastAPI, Depends
from database import get_connection
from logger import get_logger
from sql_executor import executeQuery

logger = get_logger(__name__)

if __name__=="__main__":
    print("Running main file")

    result = executeQuery("SELECT count(*) from customers", "show city of customers", 1)

    print(result["results"])
