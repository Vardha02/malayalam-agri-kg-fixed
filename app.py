import streamlit as st
from direct_qa import ask_graph

st.set_page_config(
    page_title="Malayalam Agriculture KG QA",
    page_icon="🌱"
)

st.title("🌱 Malayalam Agriculture Knowledge Graph QA")

question = st.text_input(
    "Ask your question",
    placeholder="പയറിനെ ബാധിക്കുന്ന കീടങ്ങൾ?"
)

if st.button("Ask"):
    if question.strip():
        with st.spinner("Searching..."):
            answer = ask_graph(question)
        st.success(answer)
    else:
        st.warning("Please enter a question.")