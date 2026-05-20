# 🟣 Week 3 — AI-Powered SQL Generator with FastAPI & PostgreSQL

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Natural Language → SQL → Validation → Execution**

*FuseMachines AI MicroDegree 2026 — Week 3 Assignment*

</div>

---

# 📌 About This Project

This project is an **AI-powered SQL query generation pipeline** built using **FastAPI**, **PostgreSQL**, **Docker**, and an **LLM API**.

The system accepts natural language questions, generates SQL queries using an AI model, validates the generated SQL for safety, executes it against a PostgreSQL database, and returns the results.

The project also supports **batch processing** of 50 predefined natural language SQL questions through an automated pipeline.

---

# 🚀 Features

- Convert natural language questions into SQL queries using an LLM
- Validate generated SQL before execution
- Execute SQL safely against PostgreSQL
- REST API built with FastAPI
- Batch processing pipeline for 50 SQL questions
- Dockerized full-stack setup
- Structured logging system
- Modular and scalable project architecture

---

# 📁 Project Structure

```bash
AssignmentWeek3/
│
├── app/
│   ├── agent.py                     # ⭐ Run this to start the FastAPI server
│   ├── main.py                      # ⭐ Run this to process all 50 SQL questions
│   ├── sql_generator.py             # AI-powered SQL generation
│   ├── sql_executor.py              # SQL query execution
│   ├── sql_validator.py             # SQL validation and safety checks
│   ├── database.py                  # PostgreSQL database connection
│   ├── schema.py                    # Pydantic schemas
│   ├── logger.py                    # Logging configuration
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables (not committed)
│   └── sql/
│       └── sql_questions_only.csv   # 50 natural language SQL questions
│
├── logs/
│   ├── pipeline_results.json        # Output results of all 50 questions
│   └── app.log                      # Application logs
│
├── .devcontainer/
│   └── devcontainer.json            # VS Code Dev Container configuration
│
├── docker-compose.yml               # Docker Compose configuration
├── Dockerfile                       # Docker image definition
├── seed.sql                         # Database seed data
├── .env                             # Environment variables (not committed)
└── .gitignore
```

---

# 🧠 System Workflow

```text
  Natural Language Question
            ↓
     SQL Generation (LLM)
            ↓
      SQL Validation
            ↓
      SQL Execution
            ↓
        API Response
```

---

# ⚙️ Environment Setup

Create a `.env` file inside `AssignmentWeek3/` with the following:

```env
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=db
POSTGRES_PORT=5432
API_KEY=your_llm_api_key_here
```

> ⚠️ Never commit your `.env` file to GitHub.

---

# 🐳 Running the Project

## Step 1 — Start FastAPI + PostgreSQL

```bash
cd AssignmentWeek3
docker-compose up --build
```

API Endpoint:

```bash
http://localhost:8000
```

Swagger Documentation:

```bash
http://localhost:8000/docs
```

---

# ▶️ Run the Batch Pipeline

To process all 50 natural language SQL questions:

```bash
cd AssignmentWeek3/app
python main.py
```

This will:

- Read all questions from `sql/sql_questions_only.csv`
- Generate SQL using the LLM
- Validate generated SQL
- Execute SQL against PostgreSQL
- Save outputs to:

```bash
logs/pipeline_results.json
```

---

# 📌 API Functionality

The FastAPI server allows users to:

- Send natural language SQL questions
- Generate SQL queries dynamically
- Validate generated SQL
- Execute validated SQL safely
- Return query results through REST endpoints

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Database interaction |
| Pydantic | Data validation |
| Docker & Docker Compose | Containerization |
| LLM API | Natural language to SQL generation |

---

# 📋 Prerequisites

Before running the project, ensure you have:

- Python 3.10+
- Docker & Docker Compose installed
- PostgreSQL
- A valid LLM API key

---

# 📚 Learning Outcomes

Through this project, the following concepts were implemented and practiced:

- FastAPI backend development
- AI-powered SQL generation
- SQL validation pipelines
- PostgreSQL integration
- Docker containerization
- Modular application architecture
- Logging and batch processing workflows

---

# 🧾 Output Logs

After running the pipeline, generated outputs are stored in:

```bash
logs/pipeline_results.json
```

Application logs are stored in:

```bash
logs/app.log
```

---

# 🚀 Future Improvements

- Add authentication & authorization
- Improve SQL validation security
- Support multiple database engines
- Add frontend UI for query interaction
- Streaming responses for large query outputs
- Query history and analytics dashboard

---

<div align="center">

**Built with FastAPI, PostgreSQL, Docker, and AI 🚀**

</div>
