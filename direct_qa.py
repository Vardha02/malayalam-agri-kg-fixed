from neo4j import GraphDatabase
import streamlit as st

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def ask_graph(question):
    query = """
    MATCH (a:Entity)-[r:RELATION]->(b:Entity)
    WHERE b.name CONTAINS 'നെല്ല'
      AND a.label = 'PEST'
    RETURN a.name AS name
    """

    with driver.session() as session:
        rows = session.run(query).data()

    return str(rows)