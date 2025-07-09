import sys
import os

# 👉 Optional: Print CWD for debug
print("✅ Current working dir:", os.getcwd())

# Hard-code the DB path to guarantee it’s correct
DB_PATH = "/home/ubuntu/projects/tradingbot/database/tradingbot.db"
print("✅ Using hardcoded DB path:", DB_PATH)

if not os.path.isfile(DB_PATH):
    raise FileNotFoundError(f"Database file not found at: {DB_PATH}")

# LangChain & Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_ollama import ChatOllama

# Create the LangChain SQLDatabase
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

# llm = ChatOllama(model="llama3.2:latest", temperature=0.0)
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.0,
    system="You are a SQL agent. Always return the exact query result. Do not hallucinate. Format the final answer as a JSON list of rows only."
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",    # ✅ Try structured function-calling style
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)

query = (
    "SELECT * FROM trade_history ORDER BY timestamp DESC LIMIT 5; "
    "Return the exact rows in JSON format."
)

print("\n✅ Running query:", query)

result = agent.invoke({"input": query})
print("\n✅ Agent result:", result)

print("\n✅ Direct DB fallback result:")
print(db.run(query))
# i switched models and got this

