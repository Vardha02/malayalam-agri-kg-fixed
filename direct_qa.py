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
    RETURN a.name AS name, b.name AS crop
    ORDER BY name
    """

    outputs = []

    for db in [None, "neo4j", "e3cf58ad"]:
        try:
            if db is None:
                with driver.session() as session:
                    rows = session.run(query).data()
                outputs.append(f"default DB: {rows}")
            else:
                with driver.session(database=db) as session:
                    rows = session.run(query).data()
                outputs.append(f"{db}: {rows}")
        except Exception as e:
            outputs.append(f"{db}: ERROR - {str(e)[:200]}")

    return "\n\n".join(outputs)