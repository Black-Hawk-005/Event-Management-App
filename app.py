#4
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
FIREBASE_WEB_API_KEY = "AIzaSyDPOU9vsRj04ez9SmDEK_gh5PBvhnTDsqY"

st.set_page_config(page_title="Login", layout="wide")

col1, col2 = st.columns([2, 1])

with col1:
    st.image("login-image.jpg", use_column_width=True)

with col2:
    st.markdown("<h2>Login / Sign Up</h2>", unsafe_allow_html=True)
    option = st.radio("Choose an option:", ["Sign In", "Sign Up"], horizontal=True)
    email = st.text_input("Email", key="email")
    password = st.text_input("Password", type="password", key="password")
    
    if option == "Sign Up":
        name = st.text_input("Full Name", key="name")
        role = st.radio("Register as:", ["Attendee", "Creator"], horizontal=True)
        
        if st.button("Sign Up"):
            try:
                user = auth.create_user(email=email, password=password)
                db.collection("users").document(user.uid).set({
                    "name": name,
                    "email": email,
                    "role": role
                })
                st.success("✅ Account created successfully! Please login.")
            except Exception as e:
                st.error(f"❌ {str(e)}")
    else:
        if st.button("Sign In"):
            try:
                login_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
                login_payload = {"email": email, "password": password, "returnSecureToken": True}
                response = requests.post(login_url, json=login_payload)
                
                if response.status_code == 200:
                    user_data = response.json()
                    user_doc = db.collection("users").document(user_data["localId"]).get()
                    
                    if user_doc.exists:
                        user_info = user_doc.to_dict()
                        name = user_info.get("name", "User")
                        role = user_info.get("role", "Attendee")
                        
                        st.session_state.authenticated = True
                        st.session_state.user_role = role
                        st.session_state.user_name = name

                        st.success(f"✅ Login successful! Welcome, {name} 👋")

                        if role == "Attendee":
                            st.experimental_set_query_params(page="attendees")
                        else:
                            st.experimental_set_query_params(page="organiser")
                else:
                    error_message = response.json().get("error", {}).get("message", "Unknown error")
                    st.error(f"❌ {error_message}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
