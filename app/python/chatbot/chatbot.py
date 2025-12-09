import pandas as pd
from sqlalchemy import create_engine
import requests
import json, re

# --- CONFIG ---
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- STEP 1: Connect to DB with Pandas ---
def query_db(sql_query):
    # Create SQLAlchemy engine using psycopg2 driver
    engine = create_engine("postgresql+psycopg2://docker:docker@localhost:5432/postgres")
    
    # Run query and return DataFrame
    df = pd.read_sql(sql_query, engine)
    return df


# --- STEP 2: Ask OpenRouter to translate user question into SQL ---
def generate_sql(user_question, table_schema):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4o-mini",   # pick any model available to you
        "messages": [
            {"role": "system", "content": f"You are a SQL assistant. Use this schema:\n{table_schema}"},
            {"role": "user", "content": user_question}
        ]
    }
    response = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(payload))
    sql_query = response.json()["choices"][0]["message"]["content"]

    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    sql_query = extract_sql(sql_query)

    return sql_query.strip()


def extract_sql(text):
    """
    Extracts the SQL statement from a mixed text response.
    Returns only the SQL block.
    """
    # Remove markdown fences if present
    text = text.replace("```sql", "").replace("```", "").strip()

    # Regex: capture SELECT ... ; (multi-line safe)
    match = re.search(r"(SELECT[\s\S]*?;)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("No SQL statement found")


# --- STEP 3: Main chatbot loop ---
if __name__ == "__main__":
    # Example schema (you can introspect your DB and pass it here)
    schema = """
    Table: users
    Columns: gender varchar(255),title varchar(255),	first_name varchar(255),last_name varchar(255),street_number varchar(255),street_name varchar(255),city varchar(255),state varchar(255),country varchar(255),postcode varchar(255),latitude varchar(255),longitude varchar(255),tz_offset varchar(255),tz_description varchar(255),email varchar(255),login_uuid varchar(255),username varchar(255),"password" varchar(255),dob_date varchar(255),dob_age varchar(255),registered_date varchar(255),registered_age varchar(255),phone varchar(255),cell varchar(255),id_name varchar(255),id_value varchar(255),picture_large varchar(255),picture_medium varchar(255),picture_thumbnail varchar(255),nationality varchar(255)
    """

    while True:
        user_input = input("Ask a question (or 'quit'): ")
        if user_input.lower() == "quit":
            break

        # Generate SQL from natural language
        sql = generate_sql(user_input, schema)
        print(f"Generated SQL: {sql}")

        results = query_db(sql)
        print("Answer:", results)


        # try:
        #     results = query_db(sql)
        #     print("Answer:", results)
        # except Exception as e:
        #     print("Error running query:", e)

