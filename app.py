import streamlit as st
from neo4j import GraphDatabase

st.title("Delete bad nodes")

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

if st.button("DELETE BAD NODES"):
    with driver.session() as session:
        session.run("""
        MATCH (n:Entity)
        WHERE n.name IN ['അവയുടെ', 'അല്ലെങ്കിൽ', 'ഗ്രാം', 'ഇവയുടെ']
        DETACH DELETE n
        """)

        rows = session.run("""
        MATCH (a:Entity)-[r:RELATION]->(b:Entity)
        WHERE b.name = 'ആപ്പിൾ'
        RETURN a.name AS name, a.label AS label, r.type AS rel
        """).data()

    st.success("Deleted")
    st.write(rows)