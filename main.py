import streamlit as st

app_page=st.Page(page="views/app.py",
                 title="Chat",
                 icon=":material/chat:",
                 default=True)

about_chatbot=st.Page(page="views/about_chatbot.py",
                 title="About Chatbot",
                 icon=":material/info:")

documentation=st.Page(page="views/documentation.py",
                 title="Documentation",
                 icon=":material/description:")

about_me=st.Page(page="views/about_me.py",
                 title="About Me",
                 icon=":material/person:")


pg=st.navigation(pages=[app_page,about_chatbot,documentation,about_me])

pg.run()
