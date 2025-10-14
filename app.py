#LANGCHAIN_API_KEY="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"
#GOOGLE_API_KEY=""AIzaSyClk1FI8ygKigif4kHKj_PUK_yBOfGDd8M"
#LANGCHAIN PROJECT=LANGCHAIN PROJECT

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

# -------------------------
# Explicitly load .env from absolute path
# -------------------------
dotenv_path = "/Users/sumaiyahossain/Documents/Langchain project/chatbot/.env"
load_dotenv(dotenv_path)

# -------------------------
# Get API key safely
# -------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
else:
    st.error("❌ GOOGLE_API_KEY not found. Make sure .env is in 'chatbot' folder and contains your Gemini key.")
    st.stop()  # Stop app if key is missing

# Optional LangChain/LangSmith key
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

os.environ["LANGCHAIN_TRACING_V2"] = "true"

# -------------------------
# Prompt template
# -------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's queries."),
    ("user", "Question: {question}")
])

# -------------------------
# LLM setup (Gemini v1)
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",  # Supported v1 model
    api_version="v1"          # Explicitly use v1
)

# Output parser
output_parser = StrOutputParser()

# Chain creation
chain = prompt | llm | output_parser

# -------------------------
# Streamlit UI
# -------------------------
st.title("LangChain Demo with Gemini 2.5 Pro 🤖")

input_text = st.text_input("Ask your question:")

if input_text:
    with st.spinner("Thinking..."):
        try:
            response = chain.invoke({'question': input_text})
            st.success(response)
        except Exception as e:
            st.error(f"⚠️ Error generating response: {e}")
