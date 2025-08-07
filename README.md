# 🧠 AI-Powered SQL Agent

An intelligent assistant that allows users to interact with databases using natural language. This tool leverages **LLMs** and **RAG (Retrieval-Augmented Generation)** to translate natural queries into SQL, execute them on a connected database, and return results in natural language — making data access seamless for non-technical users.

---

## 🚀 Features

- 🔍 **Natural Language Interface**: Users can ask questions in plain English.
- 🧠 **LLM + RAG**: Combines LLMs with context-aware retrieval from documentation/schema to generate accurate SQL queries.
- 🧾 **SQL Execution**: Safely queries the company’s databases.
- 🗣️ **Natural Language Output**: Converts SQL results into understandable responses.

---

## ⚙️ Tech Stack

- **LLM**: OpenAI / Local LLMs
- **RAG**: FAISS or other vector DBs for context retrieval
- **Backend**: FastAPI
- **Frontend**: React
- **Database**: SQL  (MySQL)
- **Environment**: Python, Node.js

---

## 💡 How It Works

1. **User Input**: User enters a natural language query.
2. **RAG Phase**: System retrieves relevant schema/document context from vector DB.
3. **Prompt Engineering**: Combines user query with retrieved context to form a rich prompt.
4. **LLM Interaction**: Prompt is sent to the LLM to generate an appropriate SQL query.
5. **SQL Execution**: The SQL is executed on the company’s database.
6. **Natural Response**: Result is converted back into human-readable language and returned to the user.

---

## 🧪 Example Use Case

> **User**: *"How many active users signed up this month?"*  
> 🔄 → Extracts table structure info  
> 🧠 → LLM generates SQL:  
> ```sql
> SELECT COUNT(*) FROM users WHERE status = 'active' AND signup_date >= '2025-08-01';
> ```  
> 💬 → Returns: “There are 431 active users who signed up in August.”

---
