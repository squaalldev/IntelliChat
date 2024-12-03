import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Act as a question answering chatbot."),
    ("user", "{question}")
])

# Initialize the model (LLaMA 3.1-8B)
model = ChatGroq(model="llama-3.1-8b-instant", streaming=True, groq_api_key=os.getenv("GROQ_API_KEY"))

# Set up the output parser
parser = StrOutputParser()

# Chain: Connecting the prompt template, model, and parser
chain = prompt_template | model | parser

# Streamlit interface for chatbot
st.title("QA Chatbot")

# User input via Streamlit text input
user_input = st.chat_input("Ask a question:")

# Process the user input when available
if user_input:
    # Format the prompt with the user's question
    formatted_prompt = prompt_template.format(question=user_input)
    
    # Get the response from the chain
    response = chain.invoke(formatted_prompt)
    
    # Display the response
    st.write(response)
