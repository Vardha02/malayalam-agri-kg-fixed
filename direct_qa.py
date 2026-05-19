from neo4j import GraphDatabase
import streamlit as st

URI = st.secrets["NEO4J_URI"]
USER = st.secrets["NEO4J_USERNAME"]
PASSWORD = st.secrets["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

CROPS = {
    "അമര": ["അമര", "amara", "hyacinth bean"],
    "അരി": ["അരി", "ari", "rice"],
    "ആപ്പിൾ": ["ആപ്പിൾ", "apple"],
    "ഇഞ്ചി": ["ഇഞ്ചി", "inchi", "ginger"],
    "ഉഴുന്ന്": ["ഉഴുന്ന്", "uzhunnu", "black gram"],
    "എള്ളു": ["എള്ളു", "ellu", "sesame"],
    "കടല": ["കടല", "kadala", "gram", "chickpea"],
    "കടുക്": ["കടുക്", "mustard"],
    "കപ്പ": ["കപ്പ", "tapioca", "cassava"],
    "കരിമ്പ്": ["കരിമ്പ്", "sugarcane"],
    "കറുവപ്പട്ട": ["കറുവപ്പട്ട", "cinnamon"],
    "കാന്താരി": ["കാന്താരി", "kanthari"],
    "കാപ്പി": ["കാപ്പി", "coffee"],
    "കാരറ്റ്": ["കാരറ്റ്", "carrot"],
    "കുരുമുളക്": ["കുരുമുളക്", "black pepper", "pepper"],
    "കൊക്കോ": ["കൊക്കോ", "cocoa"],
    "കോവൽ": ["കോവൽ", "ivy gourd"],
    "ഗോതമ്പ്": ["ഗോതമ്പ്", "wheat"],
    "ചക്ക": ["ചക്ക", "jackfruit"],
    "ചണ": ["ചണ", "jute"],
    "ചായ": ["ചായ", "tea"],
    "ചീര": ["ചീര", "spinach"],
    "ചുക്കു": ["ചുക്കു", "dry ginger"],
    "ചുരക്ക": ["ചുരക്ക", "bottle gourd"],
    "ചെറുപയർ": ["ചെറുപയർ", "cherupayar", "green gram"],
    "ചേന": ["ചേന", "yam"],
    "ചോളം": ["ചോളം", "maize", "corn"],
    "ജാതി": ["ജാതി", "nutmeg"],
    "തക്കാളി": ["തക്കാളി", "tomato"],
    "തിന": ["തിന", "millet"],
    "തെങ്ങ്": ["തെങ്ങ്", "coconut tree"],
    "തേങ്ങ": ["തേങ്ങ", "coconut"],
    "നാരകം": ["നാരകം", "lemon", "lime"],
    "നിലക്കടല": ["നിലക്കടല", "groundnut", "peanut"],
    "നെല്ലിക്ക": ["നെല്ലിക്ക", "amla", "gooseberry"],
    "നെല്ല്": ["നെല്ല്", "paddy", "rice"],
    "പടവലം": ["പടവലം", "snake gourd"],
    "പപ്പായ": ["പപ്പായ", "papaya"],
    "പയറു": ["പയറു", "payaru", "beans"],
    "പയർ": ["പയർ", "payar", "beans", "bean"],
    "പരുത്തി": ["പരുത്തി", "cotton"],
    "പാവൽ": ["പാവൽ", "bitter gourd"],
    "പുല്ല്": ["പുല്ല്", "grass"],
    "പേര": ["പേര", "guava"],
    "പ്ലാവ്": ["പ്ലാവ്", "jackfruit tree"],
    "ബീറ്റ്റൂട്ട്": ["ബീറ്റ്റൂട്ട്", "beetroot"],
    "ബീൻസ്": ["ബീൻസ്", "beans"],
    "മഞ്ഞൾ": ["മഞ്ഞൾ", "turmeric"],
    "മാവ്": ["മാവ്", "mango"],
    "മുളക്": ["മുളക്", "mulak", "chilli", "chili"],
    "റംബൂട്ടാൻ": ["റംബൂട്ടാൻ", "rambutan"],
    "റബ്ബർ": ["റബ്ബർ", "rubber"],
    "വഴുതന": ["വഴുതന", "brinjal", "eggplant"],
    "വാഴ": ["വാഴ", "banana"],
    "വെണ്ട": ["വെണ്ട", "okra"],
    "വെണ്ടയ്ക്ക": ["വെണ്ടയ്ക്ക", "okra", "ladies finger"],
    "സൂര്യകാന്തി": ["സൂര്യകാന്തി", "sunflower"],
    "സ്ട്രോബറി": ["സ്ട്രോബറി", "strawberry"],
}

def normalize(text):
    text = text.lower().strip()
    suffixes = ["യെ", "നെ", "ക്ക്", "യ്ക്ക്", "ിന്", "ന്", "യുടെ", "ിന്റെ", "ന്റെ", "?"]
    for s in suffixes:
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

    if any(w in q for w in ["കീട", "pest", "pests", "affect", "affects", "attack"]):
        return "PEST", "affects", "കീടങ്ങൾ"

    if any(w in q for w in ["രോഗ", "disease", "diseases"]):
        return "DISEASE", "affects", "രോഗങ്ങൾ"

    if any(w in q for w in ["വളം", "fertilizer", "fertilizers"]):
        return "FERTILIZER", "used_for", "വളങ്ങൾ"

    if any(w in q for w in ["ചികിത്സ", "treatment", "control"]):
        return "TREATMENT", "used_for", "ചികിത്സകൾ"

    return None, None, None

def ask_graph(question):
    crop = detect_crop(question)

    if not crop:
        return "NEW VERSION - വിള കണ്ടെത്താനായില്ല."

    label, relation, heading = detect_question_type(question)

    if not label:
        return f"NEW VERSION - {crop} കണ്ടെത്തി, പക്ഷേ ചോദ്യത്തിന്റെ തരം മനസ്സിലായില്ല."

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
        return f"NEW VERSION - {crop} സംബന്ധിച്ച {heading} വിവരം ലഭ്യമല്ല."

    answer = f"NEW VERSION - {crop} - {heading}:\n"

    for row in rows:
        answer += f"- {row['name']}\n"

    return answer