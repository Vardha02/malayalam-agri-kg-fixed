import streamlit as st
from neo4j import GraphDatabase

st.title("Debug Test")

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

query = """
MATCH (a:Entity)-[r:RELATION]->(b:Entity)
WHERE b.name = 'പയർ'
AND a.label = 'PEST'
AND r.type = 'affects'
RETURN a.name AS pest
ORDER BY pest
"""

with driver.session(database="neo4j") as session:
    rows = session.run(query).data()

st.write("Rows found:", len(rows))
st.write(rows)