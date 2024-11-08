import streamlit as st
from utils.auth import is_authenticated, login, logout, is_admin
from pages import home, data_analysis, predictions, create_user, account, administration, model

st.set_page_config(page_title="DstMlOpsCrypto", page_icon="📈", layout="wide")

# Custom CSS for improved layout
st.markdown("""
    <style>
    .stApp {
        margin-top: -100px;
    }
    .custom-nav-container {
        display: flex;
        justify-content: space-between;
    }
    .custom-nav {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .nav-item {
        font-size: 14px;
        justify-content: center;
        align-items: center;
    }
    .main-content {
        margin-top: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# Hide the sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Vérification de l'authentification au début
if not is_authenticated():
    st.session_state["page"] = "login"
else:
    st.session_state["page"] = st.session_state.get("page", "home")

if st.session_state["page"] == "login":
    st.title("Login Required")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("Logged in successfully!")
            st.session_state["page"] = "home"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
else:
    # Custom navigation
    pages = ["Home", "Data Analysis", "Predictions", "Account", "Model"]
    if is_admin():
        pages.extend(["Create User", "Administration"])

    st.markdown('<div class="custom-nav-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.markdown('<div class="custom-nav">', unsafe_allow_html=True)
        selection = st.selectbox("Navigation", pages, key="nav", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="nav-item">', unsafe_allow_html=True)
        st.write(f"You are logged as, {st.session_state.get('role', 'User')}: {st.session_state.get('username', 'User')}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="nav-item">', unsafe_allow_html=True)
        if st.button("Logout", key="logout"):
            logout()
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Display selected page content
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    if selection == "Home":
        home.show()
    elif selection == "Model":
        model.show()
    elif selection == "Data Analysis":
        data_analysis.show()
    elif selection == "Predictions":
        predictions.show()
    elif selection == "Account":
        account.show()
    elif selection == "Create User" and is_admin():
        create_user.show()
    elif selection == "Administration" and is_admin():
        administration.show()
    st.markdown('</div>', unsafe_allow_html=True)