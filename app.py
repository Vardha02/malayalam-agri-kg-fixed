import streamlit as st
from neo4j import GraphDatabase

st.title("Import KG to Streamlit-connected Aura")

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

if st.button("IMPORT FULL KG"):
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        session.run("""
        LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/Vardha02/agri-kg-files/main/kg_triplets_full_from_original_dataset.tsv' AS row
        FIELDTERMINATOR '\t'
        WITH row
        WHERE row.head IS NOT NULL 
          AND row.tail IS NOT NULL 
          AND row.relation IS NOT NULL

        MERGE (a:Entity {name: row.head})
        SET a.label = row.head_label

        MERGE (b:Entity {name: row.tail})
        SET b.label = row.tail_label

        MERGE (a)-[r:RELATION {type: row.relation}]->(b)
        """)

        rows = session.run("""
        MATCH (a:Entity)-[r:RELATION]->(b:Entity)
        WHERE b.name CONTAINS 'നെല്ല'
          AND a.label = 'PEST'
        RETURN a.name AS pest
        """).data()

    st.success("Import completed")
    st.write(rows)