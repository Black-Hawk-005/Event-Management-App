#6
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import qrcode
from io import BytesIO

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
query_params = st.experimental_get_query_params()
if "page" in query_params and query_params["page"][0] == "attendees":
    st.session_state.authenticated = True
    st.session_state.user_role = "Attendee"

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("❌ Access Denied! Please log in first.")
    st.stop()

if st.session_state.user_role != "Attendee":
    st.error("❌ Access Denied! You are not authorized to access this page.")
    st.stop()

st.title("🎉 Event Management - Attendees")

# Fetch available categories dynamically
categories = set()
events = db.collection("events").stream()
for event in events:
    data = event.to_dict()
    if "tag" in data:
        categories.add(data["tag"])

category_options = ["All"] + sorted(categories)
tag_filter = st.selectbox("Filter by Category:", category_options)

menu = st.sidebar.selectbox("Menu", ["Home", "Register for Event", "My Registrations", "Live Polls", "Feedback"])

if menu == "Home":
    st.subheader("Upcoming & Ongoing Events")
    events = db.collection("events").stream()
    for event in events:
        data = event.to_dict()
        st.write(f"*{data['name']}* | 📅 {data['date']}")
        st.write(data["description"])
        st.write("---")

elif menu == "Register for Event":
    st.subheader("Register for an Event")
    event_list = [e.to_dict()["name"] for e in db.collection("events").stream()]
    selected_event = st.selectbox("Select Event", event_list)
    user_email = st.text_input("Your Email")
    if st.button("Register"):
        db.collection("registrations").add({"event": selected_event, "email": user_email})
        st.success(f"Registered for {selected_event} successfully!")

elif menu == "My Registrations":
    st.subheader("My Registered Events")
    user_email = st.text_input("Enter Your Email to View Registrations")

    if st.button("Show"):
        registrations = db.collection("registrations").where("email", "==", user_email).stream()
        for reg in registrations:
            event_name = reg.to_dict()["event"]
            st.write(f"✅ {event_name}")

            # Generate QR Code for each registered event
            qr = qrcode.make(f"Event: {event_name}\nEmail: {user_email}")
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            # Display the QR code
            st.image(buffer, caption=f"QR Code for {event_name}")

            # Provide download option
            st.download_button(f"Download QR for {event_name}", buffer, file_name=f"{event_name}_qr.png", mime="image/png")


elif menu == "Live Polls":
    st.subheader("Live Event Polls & Q&A")
    event_list = [e.to_dict()["name"] for e in db.collection("events").stream()]
    selected_event = st.selectbox("Select Event", event_list)
    question = st.text_area("Post a Question")
    if st.button("Submit Question"):
        db.collection("polls").add({"event": selected_event, "question": question, "answer": ""})
        st.success("Question Submitted!")

elif menu == "Feedback":
    st.subheader("Event Feedback")
    event_list = [e.to_dict()["name"] for e in db.collection("events").stream()]
    selected_event = st.selectbox("Select Event", event_list)
    rating = st.slider("Rate the Event", 1, 5, 3)
    feedback_text = st.text_area("Your Feedback")
    if st.button("Submit Feedback"):
        db.collection("feedback").add({"event": selected_event, "rating": rating, "feedback": feedback_text})
        st.success("Feedback Submitted!")
