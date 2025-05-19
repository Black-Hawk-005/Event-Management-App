# SNUC Hacks - Event Management Platform

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

A comprehensive web-based platform designed to streamline event management workflows for hackathons and tech events. Built with Streamlit and Firebase, this solution provides organizers with powerful tools to manage attendees, track participation, and oversee event operations through an intuitive interface.

## 📋 Features

- **Secure Authentication**: Role-based access control with Firebase authentication
- **Event Management**: Create, update, and manage event details in real-time
- **Attendee Dashboard**: Comprehensive interface for participant management
- **User-Friendly Interface**: Intuitive design optimized for event organizers
- **Real-Time Updates**: Instant data synchronization for collaborative organizing

## 🔧 Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework for rapid development
- **Firebase**:
  - Authentication for secure, role-based access
  - Firestore database for scalable, real-time data storage

## 📁 File Structure

```
event-management-platform/
├── app.py                   # Main application entry point
├── pages/
│   ├── attendees.py         # Attendee management functionality
│   └── organiser.py         # Organizer dashboard and controls
├── serviceAccountKey.json   # Firebase configuration (private)
├── login-image.jpg          # UI asset for login page
└── README.md                # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Firebase account and project

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/snuc-hacks-event-platform.git
   cd snuc-hacks-event-platform
   ```

2. Install required dependencies:
   ```bash
   pip install streamlit firebase-admin
   ```

3. Set up Firebase:
   - Create a project at [firebase.google.com](https://firebase.google.com)
   - Enable Authentication and Firestore services
   - Download your service account key from Project Settings > Service Accounts
   - Save it as `serviceAccountKey.json` in the project root directory

### Running the Application

Start the application with:
```bash
streamlit run app.py
```

The platform will be accessible at `http://localhost:8501` by default.

## 📝 Notes

- This platform is designed as a prototype for internal event management at educational institutions and clubs
- For production use, additional security measures and optimizations are recommended
- Keep your `serviceAccountKey.json` private and never commit it to public repositories

## 👥 Contributors

- [Nikhilesh H](https://github.com/Nikhilesh-H)
- [Prem Danasekaran](https://github.com/Black-Hawk-005)
- [R Dhanvanyaa](https://github.com/Dhanvanyaa)
- [Ramana K S](https://github.com/Ignia707)

