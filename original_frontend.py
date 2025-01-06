# -*- coding: utf-8 -*-
# @Time    : 2025/1/6 22:55
# @Author  : Junzhe Yi
# @File    : original_frontend.py
# @Software: PyCharm

import streamlit as st
import bcrypt
import sqlite3

# Create a database connection and table
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Register user to the database
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Encrypt the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Check if the user already exists
def check_user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user is not None

# Validate user password
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    return False

# Fetch all users from the database (for admin only)
def fetch_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

# Initialize the database
create_db()

# Initialize session_state storage
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Registration page
def register():
    st.title("User Registration")

    # Input username and password
    new_user = st.text_input("Enter username", key="register_username")
    new_password = st.text_input("Enter password", type="password", key="register_password")

    if st.button("Register"):
        if check_user_exists(new_user):
            st.warning("Username already exists, please choose a different one")
        else:
            register_user(new_user, new_password)
            st.success("Registration successful!")
            st.info("Please return to the login page")

# Login page
def login():
    st.title("User Login")

    # Input username and password
    username = st.text_input("Enter username", key="login_username")
    password = st.text_input("Enter password", type="password", key="login_password")

    if st.button("Login"):
        if validate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username  # Store username in session state
            st.success(f"Welcome back, {username}!")
            st.info("You have successfully logged in")
            if username == "admin":
                st.session_state.is_admin = True  # Mark as admin
            st.rerun()  # Refresh the page and navigate to chat page
        else:
            st.error("Incorrect username or password")

# Chat page after successful login (for regular users)
def chat_page():
    st.title(f"Welcome, {st.session_state.username}!")

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Clear chat history function
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # Collect user details (Gender, Age, Profession)
    if "user_info" not in st.session_state:
        with st.sidebar.form(key="user_info_form"):
            gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
            age = st.number_input("Age", min_value=0, max_value=120, value=25)
            profession = st.text_input("Profession")
            submit_button = st.form_submit_button("Submit")

        if submit_button:
            st.session_state.user_info = {
                "gender": gender,
                "age": age,
                "profession": profession
            }
            st.rerun()  # Refresh page to hide form

    # Display user information
    if "user_info" in st.session_state:
        user_info = st.session_state.user_info
        st.sidebar.write(f"**Gender**: {user_info['gender']}")
        st.sidebar.write(f"**Age**: {user_info['age']}")
        st.sidebar.write(f"**Profession**: {user_info['profession']}")

    # Generate LLaMA2 response (placeholder function)
    def generate_llama2_response(prompt_input):
        output = "your inquery is not valid, please input valid question"  # Placeholder response
        return output

    # User input for chat
    if prompt := st.chat_input("ddd"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate new response if the last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama2_response(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

# Admin page to show all users' usernames and passwords in natural language
def admin_page():
    st.title("Admin Panel")

    users = fetch_all_users()
    if users:
        for user in users:
            username, hashed_password = user
            # Convert password to natural language description
            password_natural = f"The password for user '{username}' is securely stored in the database."
            st.write(f"Username: {username}, {password_natural}")
    else:
        st.write("No users found.")

# Main function to control page selection
def main():
    if "logged_in" in st.session_state and st.session_state.logged_in:
        if st.session_state.is_admin:
            admin_page()  # Admin page to show user data
        else:
            chat_page()  # Enter chat page after login
    else:
        st.sidebar.title("Navigation")
        choice = st.sidebar.radio("Choose page", ["Login", "Register"])

        if choice == "Login":
            login()
        elif choice == "Register":
            register()

if __name__ == '__main__':
    main()
