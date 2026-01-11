# app.py
import streamlit as st
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------
# Load FAQ / intents
# -----------------------
with open("grabfood_faq.json", "r") as f:
    faq_data = json.load(f)

questions = [item['question'] for item in faq_data]
answers = [item['answer'] for item in faq_data]

# -----------------------
# TF-IDF Vectorizer
# -----------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# -----------------------
# Menu Data
# -----------------------
menu = {
    "Fried Chicken": {"price": 12.00, "image": "images/fried_chicken.jpg"},
    "Burger": {"price": 10.00, "image": "images/burger.jpg"},
    "Nasi Lemak": {"price": 8.00, "image": "images/nasi_lemak.jpg"}
}

# -----------------------
# Session State
# -----------------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------
# Streamlit Tabs
# -----------------------
tabs = st.tabs([
    "🤖 AI Assistant",
    "🍔 Menu",
    "🛒 Cart",
    "💳 Payment",
    "ℹ️ About System"
])

# -----------------------
# TAB 1: AI Assistant
# -----------------------
with tabs[0]:
    st.header("🤖 AI Food Assistant")
    user_input = st.text_input("Ask me anything about ordering or our menu:")

    if user_input:
        user_vec = vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vec, X)
        max_idx = similarities.argmax()
        confidence = similarities[0, max_idx]

        st.write(f"**Confidence:** {confidence:.2f}")

        if confidence > 0.5:
            answer = answers[max_idx]
            st.success(answer)

            # Redirect suggestion
            if "order" in user_input.lower() or "food" in user_input.lower():
                st.info("I can help you place an order. Please select items from the 🍔 Menu tab.")
        else:
            st.warning("Sorry, I am not sure about that. Please try rephrasing your question.")

# -----------------------
# TAB 2: Menu
# -----------------------
with tabs[1]:
    st.header("🍔 Menu")
    for item, details in menu.items():
        st.image(details["image"], width=200)
        st.write(f"**{item}** - RM{details['price']:.2f}")
        if st.button(f"Add {item} to Cart"):
            st.session_state.cart.append(item)
            st.success(f"{item} added to cart!")

# -----------------------
# TAB 3: Cart
# -----------------------
with tabs[2]:
    st.header("🛒 Your Cart")
    if st.session_state.cart:
        total = 0
        for item in st.session_state.cart:
            st.write(f"- {item} - RM{menu[item]['price']:.2f}")
            total += menu[item]["price"]
        st.write(f"### Total: RM{total:.2f}")
    else:
        st.info("Your cart is empty. Go to the 🍔 Menu tab to add items!")

# -----------------------
# TAB 4: Payment
# -----------------------
with tabs[3]:
    st.header("💳 Payment (Simulated)")
    if st.session_state.cart:
        payment_method = st.radio("Select payment method:", ["Cash", "Credit/Debit Card", "E-Wallet"])
        if st.button("Confirm Payment"):
            st.success("Payment successful! 🎉")
            st.write("Your order is being prepared.")
            st.session_state.cart.clear()
    else:
        st.info("Your cart is empty. Please add items first!")

# -----------------------
# TAB 5: About System
# -----------------------
with tabs[4]:
    st.header("ℹ️ About This System")
    st.markdown("""
    **AI-Assisted Food Ordering System**  
    This system extends a conventional FAQ chatbot into a food ordering assistant.
    
    **AI Used:**  
    - Natural Language Processing with TF-IDF for intent detection  
    - Confidence-based decision support to guide ordering
    
    **Simulated Features:**  
    - Menu browsing with images  
    - Cart management  
    - Payment processing (simulated only, no real transactions)
    
    **Limitations & Ethics:**  
    - No real payment or restaurant integration  
    - Designed for demonstration and academic purposes
    """)
