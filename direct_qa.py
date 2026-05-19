from neo4j import GraphDatabase
import streamlit as st

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

ALIASES = {
    "പയർ": "പയർ",
    "പയറിനെ": "പയർ",
    "പയറിന്": "പയർ",
    "മുളക്": "മുളക്",
    "മുളകിനെ": "മുളക്",
    "കാന്താരി": "കാന്താരി",
    "ഇഞ്ചി": "ഇഞ്ചി",
    "വാഴ": "വാഴ",
    "chilli": "മുളക്",
    "chili": "മുളക്",
    "beans": "പയർ",
    "ginger": "ഇഞ്ചി",
    "banana": "വാഴ",
}

def get_crop(question):
    q = question.lower()
    for alias, crop in ALIASES.items():
        if alias.lower() in q:
            return crop
    return None

def ask_graph(question):
    crop = get_crop(question)

    if not crop:
        return "ചോദ്യത്തിലുള്ള വിളയുടെ പേര് ഗ്രാഫിൽ കണ്ടെത്താനായില്ല."

    q = question.lower()

    if "കീട" in q or "pest" in q:
        label = "PEST"
        rel = "affects"
        heading = "കീടങ്ങൾ"

    elif "രോഗ" in q or "disease" in q:
        label = "DISEASE"
        rel = "affects"
        heading = "രോഗങ്ങൾ"

    elif "വളം" in q or "fertilizer" in q:
        label = "FERTILIZER"
        rel = "used_for"
        heading = "വളങ്ങൾ"

    else:
        return "ഈ തരത്തിലുള്ള ചോദ്യം ഇപ്പോൾ പിന്തുണയ്ക്കുന്നില്ല."

    query = """
    MATCH (a:Entity)-[r:RELATION]->(b:Entity)
    WHERE b.name = $crop
      AND a.label = $label
      AND r.type = $rel
    RETURN a.name AS name
    ORDER BY name
    """

    with driver.session() as session:
        rows = session.run(
            query,
            crop=crop,
            label=label,
            rel=rel
        ).data()

    if not rows:
        return f"{crop} എന്ന വിളയ്ക്ക് {heading} സംബന്ധിച്ച വിവരം ലഭ്യമല്ല."

    answer = f"{crop} - {heading}:\n"

    for row in rows:
        answer += f"- {row['name']}\n"

    return answer