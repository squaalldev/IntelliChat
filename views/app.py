# Importing modules required for the chatbot functionality, including model setup, history management, and Streamlit UI
import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import os 

model_dict={"LLaMA 3.1-8B":"llama-3.1-8b-instant","Gemma2 9B":"gemma2-9b-it","Mixtral":"mixtral-8x7b-32768"}

# Setting up sidebar
with st.sidebar:
    st.subheader("Language Options 🌐")
    language = st.selectbox(
        "Select Language",
        ["English", "Hindi","Spanish", "French", "German"]
        )
    st.session_state.language=language
    
    with st.expander("**Model Customization**",icon="🛠️"):
    # Sidebar for model customization
        # Model type selection
        model_type = st.selectbox(
        "**Choose model type**",
        ["LLaMA 3.1-8B", "Gemma2 9B", "Mixtral"],
        help="Select the model type you want to use for generating responses. Each model has different strengths and use cases."

        )

        # Custom help for each model
        if model_type == "LLaMA 3.1-8B":
            st.session_state.model="LLaMA 3.1-8B"
            st.markdown(
                "### LLaMA 3.1-8B\n"
                "LLaMA (Large Language Model Meta AI) is a family of large language models developed by Meta. "
                "The 3.1-8B version has 8 billion parameters and is trained to be efficient in various natural language tasks, "
                "including text generation, summarization, and translation."
            )

        elif model_type == "Gemma2 9B":
            st.session_state.model="Gemma2 9B"
            st.markdown(
                "### Gemma2 9B\n"
                "Gemma2 is a powerful language model with 9 billion parameters, known for its ability to generate human-like text and perform "
                "a wide range of tasks. It is widely used for applications that require more nuanced and contextually accurate responses."
            )

        elif model_type == "Mixtral":
            st.session_state.model="Mixtral"
            st.markdown(
                "### Mixtral\n"
                "Mixtral is a multi-modal AI model designed for text and image generation tasks. It is optimized to handle a combination of natural language and "
                "visual input, allowing for creative applications in areas like design, art, and interactive storytelling."
            )

        # Temperature control
        temperature = st.slider(
            "**Temperature**",
            0.0,
            1.0,
            0.7,
            help="Controls the creativity of the model's responses. Higher values (closer to 1.0) produce more creative and diverse outputs, while lower values (closer to 0.0) result in more focused and deterministic responses."
        )
        max_tokens = st.slider(
        "**Max Tokens**",
        1,
        2048,
        512,  
        help="Controls the maximum number of tokens the model can generate in its response. Higher values allow for longer responses."
    )

greetings = {
    "English": "Hi! How can I assist you today?",
    "Spanish": "¡Hola! ¿Cómo puedo ayudarte hoy?",
    "French": "Bonjour! Comment puis-je vous aider aujourd'hui?",
    "German": "Hallo! Wie kann ich Ihnen heute helfen?",
    "Hindi": "नमस्ते! मैं आज आपकी कैसे मदद कर सकता हूँ?",
}

selected_model=model_dict[st.session_state.model]

# Initializing the language model (Llama 3.1) with streaming support for real-time responses
model = ChatGroq(model=selected_model, api_key=os.getenv("GROQ_API_KEY"),temperature=temperature,max_tokens=max_tokens, streaming=True)

# Setting up the Streamlit interface by defining the app title
st.title("Chatbot with Persistent History")

with st.chat_message(""):
    st.write(greetings[st.session_state.language])

# Initializing session state for chat history and messages to ensure conversation persistence
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()  # To store and manage message history within the session

if "messages" not in st.session_state:
    # Adding a welcome message from the assistant at the start of the session
    st.session_state.messages = []

# Defining a function to retrieve session-specific chat history for message tracking
def get_chat_history(session_id: str) -> BaseChatMessageHistory:

    # Returns the chat history for the current session
    return st.session_state.chat_history   

# Creating a prompt template to define the assistant's behavior and format its responses
generic_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer all questions to the best of your ability and give response in given {language} language."),
        MessagesPlaceholder(variable_name="messages"),  # Placeholder to dynamically include conversation history
    ]
)

# Setting up the chain to process user input and manage chat history
chain = generic_template | model
with_message_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,  # Using the chat history retrieval function
    input_messages_key="messages"  # Key to access user-provided messages
)

# Rendering chat history from session state for the user interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):  # Display messages with appropriate roles (user/assistant)
        st.write(msg["content"])  # Render the content of each message

# Capturing user input through the chat input box in Streamlit
user_input = st.chat_input("Ask a question:")

if user_input:
    # Adding the user's input to the chat history and displaying it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)  # Display the user's message in the UI

    # Generating the assistant's response using the chain and managing session ID
    response = with_message_history.invoke(
        {"language":st.session_state.language,
         "messages": [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]},
        config={"configurable": {"session_id": "default_session"}}  # Assigning a session ID for context tracking
    )

    # Adding the assistant's response to the chat history and displaying it
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    with st.chat_message("assistant"):
        st.write(response.content)  # Render the assistant's response in the UI
