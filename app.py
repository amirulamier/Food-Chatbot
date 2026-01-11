import streamlit as st
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page config
st.set_page_config(page_title="GrabFood FAQ Chatbot", layout="centered")

st.title("🍔 GrabFood Intelligent FAQ Chatbot")
st.write("Ask questions about ordering, payment, delivery, or refunds.")

# Load FAQ data
with open("grabfood_faq.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Prepare training data
questions = []
responses = []
intent_tags = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        questions.append(pattern)
        responses.append(random.choice(intent["responses"]))
        intent_tags.append(intent["tag"])

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(questions)

def get_response(user_input):
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)
    best_match = similarities.argmax()
    confidence = similarities[0][best_match]

    if confidence > 0.5:
        return responses[best_match], intent_tags[best_match], confidence
    elif confidence > 0.3:
        return (
            responses[best_match] +
            "\n\n⚠️ *This answer may not be fully accurate.*",
            intent_tags[best_match],
            confidence
        )
    else:
        return (
            "I'm not confident about that. I can help with GrabFood orders, payments, delivery time, or refunds.",
            "out_of_scope",
            confidence
        )

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", placeholder="Type your question here...")

if st.button("Send"):
    if user_input:
        reply, intent, confidence = get_response(user_input)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(
            ("Bot", f"{reply}\n\n🧠 Intent: `{intent}` | Confidence: `{confidence:.2f}`")
        )

# Display conversation
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
