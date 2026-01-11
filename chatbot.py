import streamlit as st
import json
import random

# Load FAQ data
with open("food_delivery_faq.json", "r") as file:
    data = json.load(file)

def get_response(user_input):
    user_input = user_input.lower()
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input:
                return random.choice(intent["responses"])
    return "Sorry, I didn’t quite understand that. Could you please rephrase?"

# Streamlit UI
st.set_page_config(page_title="Food Delivery FAQ Chatbot", layout="centered")

st.title("🍔 Food Delivery FAQ Chatbot")
st.write("Ask me anything about ordering, delivery, or payment.")

# Store chat history
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", placeholder="Type your question here...")

if st.button("Send"):
    if user_input:
        response = get_response(user_input)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", response))

# Display chat history
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
