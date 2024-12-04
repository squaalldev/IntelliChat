import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.agents.load_tools import load_tools
from langchain.agents.initialize import initialize_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Initialize the model (LLaMA 3.1-8B)
model = ChatGroq(model="llama-3.1-8b-instant", streaming=True)

# Set up the output parser
parser = StrOutputParser()

callback_handler = StreamlitCallbackHandler(st.container())

serp_tool = load_tools(["serpapi"])
agent = initialize_agent(
    tools=serp_tool,
    llm=model,
    agent="zero-shot-react-description",
    verbose=False,
    handle_parsing_errors=True,
    callbacks=[callback_handler],  # Streamlit callback for streaming
)

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

# Get the response from the agent
    try:
        with st.chat_message("assistant"):
            response = agent.invoke(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            print(response)
            st.write(response)
    except Exception as e:
        # Handle errors gracefully
        error_message = f"An error occurred: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        with st.chat_message("assistant"):
            st.write(error_message)