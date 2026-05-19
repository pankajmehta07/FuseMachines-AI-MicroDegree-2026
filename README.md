# 🤖 FuseMachines AI MicroDegree 2026

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

**A hands-on journey through Artificial Intelligence and Machine Learning**
*FuseMachines AI MicroDegree Program — 2026 Cohort*

</div>

---

## 📌 About This Repository

This repository contains all coursework, assignments, and solutions completed as part of the **FuseMachines AI MicroDegree Program (2026)**. The program is a structured, project-based AI education initiative by [Fusemachines](https://fusemachines.com), progressing from Python & data wrangling in Week 1 to building production-style FastAPI + PostgreSQL + Docker applications in Weeks 2 and 3.

---

## 📁 Repository Structure

    FuseMachines-AI-MicroDegree-2026/
    │
    ├── Week1/                                          # Data Wrangling & SQL
    │   ├── Wk_1_Data_Wrangling_HeartAttack.ipynb      # Main Jupyter Notebook
    │   ├── Wk_1_Data_Wrangling_HeartAttack.pdf        # Assignment PDF
    │   ├── clinical_data.csv                           # Dataset
    │   ├── lifestyle_factors.csv                       # Dataset
    │   ├── patient_demographics.csv                    # Dataset
    │   ├── mysqlsampledatabase.sql                     # SQL sample database
    │   ├── SQL Assignment.docx                         # SQL assignment doc
    │   ├── Week 1 SQL Assignment.pdf                   # SQL assignment PDF
    │   └── source/                                     # Source/reference materials
    │
    ├── Week2/                                          # FastAPI + PostgreSQL + Docker
    │   ├── Task1_Week2.pdf                             # Task descriptions
    │   ├── Task2_Week2.pdf
    │   ├── Task3_Week2.pdf
    │   └── AssignmentWeek2/
    │       ├── app/
    │       │   ├── main.py                             # FastAPI entry point
    │       │   ├── models.py                           # SQLAlchemy models
    │       │   ├── schemas.py                          # Pydantic schemas
    │       │   ├── crud.py                             # CRUD operations
    │       │   ├── database.py                         # DB connection setup
    │       │   ├── router.py                           # API routes
    │       │   ├── counts_router.py                    # Count-based routes
    │       │   ├── logger.py                           # Logging setup
    │       │   ├── app.log                             # Log file
    │       │   └── requirements.txt                    # Python dependencies
    │       ├── .devcontainer/
    │       │   └── devcontainer.json                   # VS Code dev container config
    │       ├── docker-compose.yml                      # Docker Compose config
    │       ├── Dockerfile                              # Docker image definition
    │       ├── seed.sql                                # Database seed data
    │       ├── .env                                    # Environment variables (not committed)
    │       └── .gitignore
    │
    ├── Week3/                                          # AI-Powered SQL Generator
    │   ├── Week3_Task1_Assignment.pdf                  # Task descriptions
    │   ├── Week3_Task2_Assignment.pdf
    │   ├── Week3_Task3_Assignment.pdf
    │   ├── Week3_Task4_Assignment.pdf
    │   ├── seed.sql                                    # Database seed data
    │   ├── Task Docs Solutions/                        # Submitted solution documents
    │   │   ├── Task 1 Part 1.pdf
    │   │   └── Task 2.pdf
    │   └── AssignmentWeek3/
    │       ├── app/
    │       │   ├── agent.py                            # ⭐ Run this for the FastAPI server
    │       │   ├── main.py                             # ⭐ Run this to process all 50 SQL questions
    │       │   ├── sql_generator.py                    # AI-powered SQL generation
    │       │   ├── sql_executor.py                     # SQL execution logic
    │       │   ├── sql_validator.py                    # SQL validation logic
    │       │   ├── database.py                         # DB connection setup
    │       │   ├── schema.py                           # Pydantic schemas
    │       │   ├── logger.py                           # Logging setup
    │       │   ├── requirements.txt                    # Python dependencies
    │       │   ├── .env                                # App-level env variables (not committed)
    │       │   └── sql/
    │       │       └── sql_questions_only.csv          # 50 natural language SQL questions
    │       ├── logs/
    │       │   └── pipeline_results.json               # Output log of all 50 question given for assignment
    │       │   └── app.log                             # Log file
    │       ├── .devcontainer/
    │       │   └── devcontainer.json                   # VS Code dev container config
    │       ├── docker-compose.yml                      # Docker Compose config
    │       ├── Dockerfile                              # Docker image definition
    │       ├── seed.sql                                # Database seed data
    │       ├── .env                                    # Environment variables (not committed)
    │       └── .gitignore
    │
    └── .gitignore

---

## 📅 Weekly Breakdown

### 🟢 Week 1 — Data Wrangling & SQL

> *Exploring and cleaning real-world medical datasets using Python and SQL.*

**Topics Covered:**
- Data wrangling with **Pandas**: loading, cleaning, merging, and transforming datasets
- Exploratory Data Analysis (EDA) on a Heart Attack dataset
- Handling missing values, data type conversion, and feature exploration
- **SQL** fundamentals and querying using a sample MySQL database

**Key Files:**
- `Wk_1_Data_Wrangling_HeartAttack.ipynb` — main notebook with full EDA and wrangling
- `clinical_data.csv`, `lifestyle_factors.csv`, `patient_demographics.csv` — datasets used
- `mysqlsampledatabase.sql` — SQL database for the SQL assignment

**Running Week 1:**

    cd Week1
    pip install pandas matplotlib seaborn jupyter
    jupyter notebook

Then open `Wk_1_Data_Wrangling_HeartAttack.ipynb`.

---

### 🔵 Week 2 — REST API with FastAPI, PostgreSQL & Docker

> *Building a production-style REST API backed by PostgreSQL, containerized with Docker.*

**Topics Covered:**
- Building REST APIs with **FastAPI**
- Database modeling and ORM with **SQLAlchemy**
- Data validation with **Pydantic** schemas
- Connecting to **PostgreSQL** running inside Docker
- Structuring a project with routers, CRUD operations, and logging
- Containerizing the full application with **Docker** and **Docker Compose**

**Key Files:**
- `app/main.py` — FastAPI app entry point
- `app/models.py` — database table definitions
- `app/schemas.py` — request/response validation
- `app/crud.py` — database operations
- `app/router.py` & `app/counts_router.py` — API route handlers
- `app/database.py` — PostgreSQL connection
- `docker-compose.yml` — spins up FastAPI + PostgreSQL together
- `seed.sql` — pre-populates the database with initial data

**⚙️ Environment Setup**

Create a `.env` file inside `Week2/AssignmentWeek2/` with the following:

    POSTGRES_USER=your_postgres_username
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB=your_database_name
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

**Running Week 2:**

    cd Week2/AssignmentWeek2
    docker-compose up --build

API → `http://localhost:8000`
Swagger Docs → `http://localhost:8000/docs`

---

### 🟣 Week 3 — AI-Powered SQL Generator with FastAPI & PostgreSQL

> *Building an intelligent pipeline that takes natural language input, generates SQL using an AI model, validates it, and executes it against a PostgreSQL database.*

**Topics Covered:**
- AI-powered **natural language to SQL** generation using an LLM API
- SQL validation and safe execution pipelines
- Building an **AI agent** (`agent.py`) to serve the FastAPI endpoints
- Batch processing of 50 natural language questions sequentially via `main.py`
- Advanced FastAPI project structure with modular components
- PostgreSQL + Docker Compose setup
- Logging pipeline results to `logs/pipeline_results.json`

**Key Files:**

| File | Purpose |
|---|---|
| `app/agent.py` | ⭐ **Start the FastAPI server** — run this to launch the API |
| `app/main.py` | ⭐ **Batch runner** — reads all 50 questions from the CSV and runs them sequentially |
| `app/sql_generator.py` | Sends natural language prompts to the LLM, returns SQL queries |
| `app/sql_validator.py` | Validates the generated SQL before execution |
| `app/sql_executor.py` | Safely executes validated SQL against PostgreSQL |
| `app/database.py` | PostgreSQL connection setup |
| `app/schema.py` | Pydantic request/response schemas |
| `app/sql/sql_questions_only.csv` | The 50 natural language questions (one per line) |
| `logs/pipeline_results.json` | Output log — results of all 50 questions after running `main.py` |
| `docker-compose.yml` | Spins up FastAPI + PostgreSQL together |
| `seed.sql` | Pre-populates the database for query testing |
| `Task Docs Solutions/` | Submitted PDF solution documents for the assignment |

**⚙️ Environment Setup**

Create a `.env` file inside `Week3/AssignmentWeek3/` with the following:

    POSTGRES_USER=your_postgres_username
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB=your_database_name
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    API_KEY=your_llm_api_key_here

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

**Running Week 3:**

**Step 1** — Start the full stack (FastAPI + PostgreSQL) with Docker:

    cd Week3/AssignmentWeek3
    docker-compose up --build

API → `http://localhost:8000`
Swagger Docs → `http://localhost:8000/docs`

**Step 2** — To run all 50 SQL questions sequentially from the CSV:

    cd Week3/AssignmentWeek3/app
    python main.py

This reads every question from `sql/sql_questions_only.csv` line by line, sends each one through the full pipeline (generate → validate → execute), and saves all results to `logs/pipeline_results.json`.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **Jupyter Notebook** | Data wrangling and EDA (Week 1) |
| **Pandas** | Data manipulation and analysis |
| **FastAPI** | REST API framework (Weeks 2 & 3) |
| **SQLAlchemy** | ORM for database modeling |
| **Pydantic** | Data validation and schemas |
| **PostgreSQL** | Relational database |
| **Docker & Docker Compose** | Containerization and orchestration |
| **LLM API** | AI-powered SQL generation (Week 3) |

---

## 📋 Prerequisites

- Python 3.10+
- Docker & Docker Compose installed
- A valid LLM API key (for Week 3)
- Jupyter Notebook (for Week 1 only)

---

## 📚 Resources & References

- [FuseMachines Official Website](https://fusemachines.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

<div align="center">
<i>Built with curiosity, debugged with patience. 🚀</i>
</div>
