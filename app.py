import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages.human import HumanMessage
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.string import StrOutputParser
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the model (LLaMA 3.1-8B)
model = ChatGroq(model="llama-3.1-8b-instant", streaming=True)

# Store for session-specific histories
store = {}

# Function to get session-specific chat history
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Wrap the model with chat history management

# Set up the prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Act as a question answering chatbot.")
])

contextualize_q_system_prompt=(
            "Given a chat history and the latest user question"
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

with_message_history = RunnableWithMessageHistory(model,
                                                  get_session_history,
                                                  history_messages_key="chat_history",
                                                  output_messages_key="answer")


# Streamlit UI Setup
st.title("QA Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

# Display the chat history from session state
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get user input
user_input = st.chat_input("Ask a question:")

if user_input:
    # Add user input to the chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Fetch chat history for the current session
    session_id = "chat1"
    config = {"configurable": {"session_id": session_id}}

    # Generate response using the model and history
    response = with_message_history.invoke({"input":user_input,"chat_history":st.session_state['messages']}, config=config)

    # Add assistant's response to the chat history
    st.session_state["messages"].append({"role": "assistant", "content": response.content})

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.write(response['answer'])
