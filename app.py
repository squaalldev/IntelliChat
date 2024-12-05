import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages.human import HumanMessage
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the model
model = ChatGroq(model="llama-3.1-8b-instant", streaming=True)

# Initialize Streamlit app
st.title("Chatbot with Persistent History")

# Initialize session state for messages and history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm your assistant. How can I help you today?"}
    ]

# Define a function to retrieve the session-specific chat history
def get_chat_history(session_id: str) -> BaseChatMessageHistory:
    return st.session_state.chat_history

# Define the prompt template
generic_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Set up the chain with chat history management
chain = generic_template | model
with_message_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="messages"
)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask a question:")

if user_input:
    
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate assistant response with session_id
    response = with_message_history.invoke(
        {"messages": [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]},
        config={"configurable": {"session_id": "default_session"}}  # Ensure session_id is set
    )

    # Append assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    with st.chat_message("assistant"):
        st.write(response.content)
