#7
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
query_params = st.experimental_get_query_params()
if "page" in query_params and query_params["page"][0] == "organiser":
    st.session_state.authenticated = True
    st.session_state.user_role = "Creator"

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Access Denied! Please log in first.")
    st.stop()

if st.session_state.user_role != "Creator":
    st.error("❌ Access Denied! You are not authorized to access this page.")
    st.stop()

st.title("🎉 Event Management - Organizers")

menu = st.sidebar.selectbox("Menu", ["Create Event", "Live Polls", "Feedback & Analytics"])

if menu == "Create Event":
    st.subheader("Create a New Event")
    name = st.text_input("Event Name")
    date = st.date_input("Event Date")
    description = st.text_area("Description")

    # Fetch existing categories
    categories = set()
    events = db.collection("events").stream()
    for event in events:
        data = event.to_dict()
        if "tag" in data:
            categories.add(data["tag"])

    category_options = sorted(categories) + ["Add New Category"]
    selected_category = st.selectbox("Event Category", category_options)

    new_category = None
    if selected_category == "Add New Category":
        new_category = st.text_input("Enter New Category")

    if st.button("Create Event"):
        final_category = new_category if new_category else selected_category
        if final_category:
            db.collection("events").add({
                "name": name,
                "date": date.strftime("%Y-%m-%d"),
                "description": description,
                "tag": final_category
            })
            st.success("Event Created Successfully!")
