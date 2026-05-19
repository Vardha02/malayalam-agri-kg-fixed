from neo4j import GraphDatabase
import streamlit as st

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

CROPS = {
    "പയർ": ["പയർ", "പയറ", "beans", "bean"],
    "മുളക്": ["മുളക്", "മുളക", "chilli", "chili", "pepper"],
    "കാന്താരി": ["കാന്താരി", "കാന്താര", "kanthari"],
    "ഇഞ്ചി": ["ഇഞ്ചി", "ഇഞ്ച", "ginger"],
    "വാഴ": ["വാഴ", "banana"],
}

def normalize(text):
    text = text.lower().strip()
    for s in ["യെ", "നെ", "ക്ക്", "യ്ക്ക്", "ിന്", "ന്", "യുടെ", "ിന്റെ", "ന്റെ", "?"]:
        text = text.replace(s, "")
    return text

def detect_crop(question):
    q = normalize(question)
    for crop, aliases in CROPS.items():
        for alias in aliases:
            if normalize(alias) in q:
                return crop
    return None

def detect_question_type(question):
    q = question.lower()
    if any(w in q for w in ["കീട", "pest", "pests", "affect", "affects"]):
        return "PEST", "affects", "കീടങ്ങൾ"
    if any(w in q for w in ["രോഗ", "disease", "diseases"]):
        return "DISEASE", "affects", "രോഗങ്ങൾ"
    if any(w in q for w in ["വളം", "fertilizer", "fertilizers"]):
        return "FERTILIZER", "used_for", "വളങ്ങൾ"
    return None, None, None

def ask_graph(question):
    crop = detect_crop(question)
    if not crop:
        return "വിള കണ്ടെത്താനായില്ല."

    label, relation, heading = detect_question_type(question)
    if not label:
        return "ചോദ്യത്തിന്റെ തരം മനസ്സിലായില്ല."

    query = """
    MATCH (a:Entity)-[r:RELATION]->(b:Entity)
    WHERE b.name = $crop
      AND a.label = $label
      AND r.type = $relation
    RETURN DISTINCT a.name AS name
    ORDER BY name
    """

    with driver.session() as session:
        rows = session.run(query, crop=crop, label=label, relation=relation).data()

    if not rows:
        return f"{crop} സംബന്ധിച്ച {heading} വിവരം ലഭ്യമല്ല."

    answer = f"{crop} - {heading}:\n"
    for row in rows:
        answer += f"- {row['name']}\n"
    return answer