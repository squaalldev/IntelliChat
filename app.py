import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
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
model = ChatGroq(model="llama-3.1-8b-instant", streaming=True,
                 groq_api_key=os.getenv("GROQ_API_KEY"))

# Set up the output parser
parser = StrOutputParser()

callback_handler = StreamlitCallbackHandler(st.container())
# Chain: Connecting the prompt template, model, and parser
chain = prompt_template | model | parser

# Streamlit interface for chatbot
st.title("QA Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
    ]
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])
# User input via Streamlit text input
user_input = st.chat_input("Ask a question:")

# Process the user input when available
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    st.chat_message("user").write(user_input)

    # Format the prompt with the user's question
    formatted_prompt = prompt_template.format(question=user_input)

    # Get the response from the chain
    response = chain.invoke(formatted_prompt)

    st.session_state.messages.append({"role":"ai","content":response})

    # Display the response
    with st.chat_message("ai"):
        st.write(response)