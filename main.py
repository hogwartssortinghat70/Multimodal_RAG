import os
import sqlite3
import pandas as pd
import json
import requests
from typing import Optional, List

# --- LangChain Imports for Google/Gemini ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
# -------------------------------------------


# --- 2. Extract schema and unique values function ---
def extract_structure_and_unique_values(dbpath, max_values=20):
    """
    Extracts table structure and a list of distinct values for each column.
    Provides rich context to the LLM.
    """
    schema_dict = {}
    try:
        with sqlite3.connect(dbpath) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [row[0] for row in cursor.fetchall()]

            for table in tables:
                schema_dict[table] = {}

                cursor.execute(f'PRAGMA table_info("{table}")')
                columns = [row[1] for row in cursor.fetchall()]

                for col in columns:
                    try:
                        # Fetch distinct non-null values
                        query = f'SELECT DISTINCT "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL LIMIT {max_values}'
                        df = pd.read_sql_query(query, connection)
                        unique_values = df.iloc[:, 0].dropna().astype(str).tolist()
                        schema_dict[table][col] = unique_values
                    except Exception as e:
                        schema_dict[table][col] = [f"Error fetching values: {e}"]
    except Exception as e:
        return f"Error extracting schema: {e}"

    return json.dumps(schema_dict, indent=2)


# --- 4. Custom prompt prefix builder (The template for context injection) ---
def build_custom_prompt_prefix():
    """
    Defines the strict instructions and includes a {table_info} placeholder
    for manual schema injection.
    """
    prompt_prefix = """
You are an expert SQLite SQL analyst, connected to a database containing 'Respondent' and 'Household_members' tables.

You MUST use the provided database schema and unique value information below to construct your SQL queries.

Database Schema and Context:
---
{table_info}
---

Follow these strict rules:
1. Use **double quotes** around all table and column names (e.g., `"table"`).
2. For age grouping (e.g., 10-20), use a **CASE statement** on `CAST("Age" AS REAL)`.
3. Plan your steps using Thought/Action/Action Input.
4. The provided context includes all necessary column names. Do not rely on the `sql_db_schema` tool.
5. **CRITICAL:** After running the SQL query and receiving the Observation, your next step MUST be to generate a Final Answer in the exact required format: 'Final Answer: [Your summarized results]'.
6. while generating the sql query check the semicolon and syntax carefully at action input step you sometimes put double semicolon at the end.
"""
    return prompt_prefix


# --- 5. Initialize LangChain SQL Agent with Gemini LLM (FINAL WORKING FIX) ---
def initialize_sql_agent(db_path, api_key):
    if not api_key:
        print("ERROR: GOOGLE_API_KEY is not set.")
        return None

    # 1. Initialize DB Connection
    db = SQLDatabase.from_uri(
        f"sqlite:///{db_path}",
        include_tables=["Respondent", "Household_members"],
        sample_rows_in_table_info=False
    )

    # 2. Extract full schema and unique values (manual context creation)
    custom_schema_json = extract_structure_and_unique_values(db_path)
    base_table_info = db.get_table_info()

    # Combine the base definition with the detailed unique value context
    full_table_info = f"""
    --- BASE TABLE DEFINITION ---
    {base_table_info}
    --- DETAILED COLUMN & UNIQUE VALUES ---
    {custom_schema_json}
    """

    # 3. Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.0
    )

    # 4. Initialize the standard SQL Toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # 5. Build the custom prefix with the manually formatted schema
    prompt_prefix_template = build_custom_prompt_prefix()
    final_prefix_with_schema = prompt_prefix_template.format(table_info=full_table_info)

    # 6. Construct the full LangChain Prompt Template (as a string)
    # FIX: Replaced {intermediate_steps} with the mandatory {agent_scratchpad}
    full_prompt_template_string = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query to run, then look at the results and return the final answer.
Unless the user specifies a number of examples they wish to obtain.

{final_prefix_with_schema}

You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought:{agent_scratchpad}
"""

    # 7. Create the final PromptTemplate object
    final_prompt_object = PromptTemplate.from_template(
        template=full_prompt_template_string,
        # FIX: Removed redundant 'input_variables'
        partial_variables={"final_prefix_with_schema": final_prefix_with_schema}
    )

    # 8. Create the SQL Agent using the PROMPT parameter
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="zero-shot-react-description",
        handle_parsing_errors=True,
        max_iterations=8,
        # FIX: Use 'prompt' instead of 'prefix'
        prompt=final_prompt_object
    )
    return agent_executor


# --- 9. Main Execution Example (Modified for Interactive Input) ---
if __name__ == "__main__":
    # 🔑 IMPORTANT: Replace with your actual database and API key
    DB_PATH = os.getenv("DB_PATH", "/workspaces/M/sample.db")  # Default to a local path
    # Use your Google/Gemini API Key here.
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY environment variable is not set.")
        exit(1)

    agent = initialize_sql_agent(DB_PATH, GOOGLE_API_KEY)

    if agent:
        print("\n--- SQL Agent Interactive Mode ---")
        print("Type your database question and press Enter. Type 'exit' or 'quit' to end the session.")


        # Start the interactive loop
        while True:

            # Get user input
            user_input = input("\nQuery (or 'exit'): ").strip()

            # Check for exit commands
            if user_input.lower() in ['exit', 'quit','bye']:
                print("\nSession ended. Goodbye!")
                break

            if not user_input:
                continue

            try:
                print(f"\n--- Processing Query: {user_input} ---\n")

                # Invoke the agent
                result = agent.invoke({"input": user_input})

                # Print the final output cleanly
                if isinstance(result, dict) and "output" in result:
                    print("\n" + "="*50)
                    print("="*50)
                    print(result["output"].strip())
                else:
                    print(result)

            except Exception as e:
                print(f"\n🛑 Error in agent execution: {e}")
                print("Please try rephrasing your query or checking your connection/quota.")