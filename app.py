import streamlit as st
from direct_qa import ask_graph

st.set_page_config(page_title="Malayalam Agri QA")

st.title("🌱 Malayalam Agriculture QA")

question = st.text_input("Ask a question")

if st.button("Ask"):
    if question:
        answer = ask_graph(question)
        st.write(answer)