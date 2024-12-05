import streamlit as st

# Setting the title for the page
st.title("About Me")

# Introduction Section
st.header("👋 Introduction")
st.write("""
Hello there! I'm Mitesh Gupta, a passionate Machine Learning enthusiast and developer.
I love building innovative AI solutions and exploring the latest advancements in deep learning, generative AI, and NLP.
Feel free to connect and explore my projects!
""")

# Skills Section
st.header("🚀 Skills")
st.markdown("""
- **Programming Languages**: Python
- **AI/ML Frameworks**: TensorFlow, PyTorch, LangChain
- **Tools**: Streamlit, Hugging Face, OpenAI APIs
- **Other Skills**: Data Science, Deep Learning, NLP, Generative AI, RAG Systems
""")

# Interests Section
st.header("🌟 Interests")
st.markdown("""
- **AI Research**: Staying updated with state-of-the-art AI models and research papers.
- **Projects**: Working on innovative tools like chatbots, dashboards, and RAG systems.
- **Community**: Sharing knowledge through blogs and contributing to open-source projects.
""")

# Contact Section
st.header("📬 Contact Me")

st.markdown("""
<div align="left">
  <a href="mailto:your_email@gmail.com" target="blank"><img align="center" src="https://github.com/tandpfun/skill-icons/blob/main/icons/Gmail-Dark.svg" alt="gmail" height="40" width="40" /></a> &nbsp;
  <a href="https://linkedin.com/in/your-profile" target="blank"><img align="center" src="https://github.com/tandpfun/skill-icons/blob/main/icons/LinkedIn.svg" alt="linkedin" height="40" width="40" /></a> &nbsp;
  <a href="https://twitter.com/your-profile" target="blank"><img align="center" src="https://github.com/tandpfun/skill-icons/blob/main/icons/Twitter.svg" alt="twitter" height="40" width="40" /></a> &nbsp;
  <a href="https://github.com/your-github" target="blank"><img align="center" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="github" height="40" width="40" /></a>
</div>
""", unsafe_allow_html=True)

# Closing Section
st.write("Thank you for visiting my chatbot application. Let’s build something amazing together!")
