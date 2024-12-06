import streamlit as st

# Setting the title for the page
st.title("Documentation 📃")

# Overview Section
st.header("Overview")
st.write("""
This chatbot is designed to assist users by answering their queries in a conversational format.
The project is built using the following technologies:
- **Streamlit**: For creating an interactive web interface.
- **ChatGroq**: A robust conversational AI backend.
- **Python**: Core programming language for logic and integration.
""")

# How to Use the Chatbot Section
st.header("How to Use the Chatbot")
st.write("""
To use the chatbot:
1. Select the model type and customize parameters from the sidebar.
2. Enter your query in the chat input box and get instant responses.
3. View your conversation history directly in the chat interface.
""")
st.markdown("**Example Queries:**")
st.write("- `Who is Elon Musk ?`")
st.write("- `Explain the concept of persistent chat history.`")

# Features Section
st.header("Features")
st.write("""
The chatbot provides the following features:
- **Persistent Conversation History**: Maintains the flow of conversation.
- **Customizable Models**: Adjust parameters like temperature and max tokens.
- **File Upload Support**: Upload PDFs or DOCX files for document-based question answering.
""")

# FAQs Section
st.header("FAQs")
st.markdown("""
**Q: How can I reset the conversation history?**  
A: Simply refresh the page to start a new session with an empty chat history.

**Q: Can I use this chatbot for multiple types of queries?**  
A: Yes,general knowledge, or any topic supported by the chosen model.
""")

# Acknowledgments Section
st.header("Acknowledgments")
st.write("""
This project was made possible with the following resources:
- **LangChain**: For managing chat history and prompts.
- **Groq Models**: High-performance conversational AI models.
""")

# Footer Section
st.write("For further details, please refer to the [project repository](https://github.com/miteshgupta07/QA-Chatbot) or contact me through the links provided on the '**About Me**' page.")