import streamlit as st
from service_desk import ServiceDesk
import pandas as pd
import os

# Initialize ServiceDesk
service_desk = ServiceDesk()

# Load the classifier if it exists
if os.path.exists('service_desk_classifier.joblib'):
    service_desk.load_classifier()

st.title("Cognitive IT Service Desk")

# Sidebar for admin functions
st.sidebar.header("Admin Functions")
if st.sidebar.button("Train Classifier"):
    service_desk.train_classifier()
    st.sidebar.success("Classifier trained successfully!")

if st.sidebar.button("Generate Insights"):
    common_issues, performance_metrics = service_desk.generate_insights()
    st.sidebar.subheader("Common Issues")
    st.sidebar.write(common_issues)
    st.sidebar.subheader("Performance Metrics")
    st.sidebar.write(performance_metrics)

# Main chat interface
st.header("Chat with IT Support")
user_input = st.text_input("Type your issue here:")

if user_input:
    response = service_desk.handle_user_query(user_input)
    st.text_area("IT Support Response:", value=response, height=100, max_chars=None, key=None)

# Ticket submission form
st.header("Submit a Ticket")
name = st.text_input("Your Name:")
email = st.text_input("Your Email:")
issue_title = st.text_input("Issue Title:")
issue_description = st.text_area("Issue Description:")
priority = st.selectbox("Priority:", ["Low", "Medium", "High"])

if st.button("Submit Ticket"):
    ticket = service_desk.create_ticket(name,email,issue_title, issue_description, priority)
    st.success(f"Ticket created successfully! Ticket ID: {ticket['id']}")

# Display recent tickets
st.header("Recent Tickets")
recent_tickets = service_desk.get_recent_tickets()
st.table(pd.DataFrame(recent_tickets))