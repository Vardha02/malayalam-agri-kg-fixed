from neo4j import GraphDatabase
import streamlit as st

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

CROP_ALIASES = {
    "പയർ": "പയർ",
    "beans": "പയർ",
    "bean": "പയർ",

    "മുളക്": "മുളക്",
    "chilli": "മുളക്",
    "chili": "മുളക്",
    "pepper": "മുളക്",

    "കാന്താരി": "കാന്താരി",

    "ഇഞ്ചി": "ഇഞ്ചി",
    "ginger": "ഇഞ്ചി",

    "വാഴ": "വാഴ",
    "banana": "വാഴ",
}

def detect_crop(question):
    q = question.lower()

    for alias, crop in CROP_ALIASES.items():
        if alias.lower() in q:
            return crop

    for crop in ["പയർ", "മുളക്", "കാന്താരി", "ഇഞ്ചി", "വാഴ"]:
        if crop in question:
            return crop

    return None


def detect_question_type(question):
    q = question.lower()

    pest_words = [
        "കീട", "pest", "pests", "affect", "affects", "attack"
    ]

    disease_words = [
        "രോഗ", "disease", "diseases"
    ]

    fertilizer_words = [
        "വളം", "fertilizer", "fertilisers", "fertilizers"
    ]

    treatment_words = [
        "ചികിത്സ", "treatment", "control"
    ]

    if any(word in q for word in pest_words):
        return "PEST", "affects", "കീടങ്ങൾ"

    if any(word in q for word in disease_words):
        return "DISEASE", "affects", "രോഗങ്ങൾ"

    if any(word in q for word in fertilizer_words):
        return "FERTILIZER", "used_for", "വളങ്ങൾ"

    if any(word in q for word in treatment_words):
        return "TREATMENT", "used_for", "ചികിത്സകൾ"

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
        rows = session.run(
            query,
            crop=crop,
            label=label,
            relation=relation
        ).data()

    if not rows:
        return f"{crop} സംബന്ധിച്ച {heading} വിവരം ലഭ്യമല്ല."

    answer = f"{crop} - {heading}:\n"

    for row in rows:
        answer += f"- {row['name']}\n"

    return answer