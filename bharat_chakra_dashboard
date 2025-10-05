import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Mock data from Knowledge Base
constituencies = pd.DataFrame({
    "State": ["Uttar Pradesh", "Maharashtra"],
    "PC": ["Varanasi", "Mumbai North"],
    "Winning_Probability": [75, 60],
    "Anti_Incumbency_Score": [40, 55],
    "Sentiment_Index": [0.6, 0.4],
    "Demographics": [{"Caste": "General:50%, OBC:30%"}, {"Caste": "General:40%, SC:20%"}]
})

def predict_win_prob(feature):
    try:
        model = LogisticRegression()
        X = np.array([[1], [2], [3], [4]])
        y = np.array([0, 0, 1, 1])
        model.fit(X, y)
        return model.predict_proba(np.array([[feature]]))[0][1] * 100
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return 50.0

# Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = st.sidebar.selectbox("Role", ["National Admin", "Client", "Campaign Manager", "Field Manager", "Booth Worker"])
    if st.sidebar.button("Login"):
        st.session_state.logged_in = True
        st.session_state.role = role
        st.rerun()

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title(f"Welcome, {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    def check_access(level):
        roles = {"National Admin": 5, "Client": 4, "Campaign Manager": 3, "Field Manager": 2, "Booth Worker": 1}
        return roles.get(st.session_state.role, 0) >= level

    st.title("Bharat Chakra Dashboard")
    st.markdown("""
        <style>
        .stApp { background-color: #121212; color: #FFFFFF; }
        .stButton>button { border: 2px solid #00E5FF; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); color: #00E5FF; }
        .stSelectbox { border: 1px solid #7B61FF; }
        </style>
    """, unsafe_allow_html=True)

    if check_access(3):
        st.header("Interactive GIS Map")
        kpi = st.selectbox("KPI for Coloring", ["Winning_Probability", "Anti_Incumbency_Score", "Sentiment_Index"])
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        folium.GeoJson({
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "properties": {"name": "Uttar Pradesh", "kpi": constituencies.iloc[0][kpi]}, "geometry": {"type": "Polygon", "coordinates": [[[80,25],[82,26],[81,24]]]}},
                {"type": "Feature", "properties": {"name": "Maharashtra", "kpi": constituencies.iloc[1][kpi]}, "geometry": {"type": "Polygon", "coordinates": [[[75,19],[77,20],[76,18]]]}}
            ]
        }, style_function=lambda feature: {
            'fillColor': 'green' if feature['properties']['kpi'] > 60 else 'red',
            'color': 'black',
            'weight': 1
        }).add_to(m)
        folium_static(m)

        state = st.selectbox("Filter by State", constituencies["State"].unique())
        if st.button("Drill Down"):
            st.session_state.selected_const = constituencies[constituencies["State"] == state].iloc[0]

    st.header("Political Weather Overview")
    st.metric("Election Countdown", "30 days to Lok Sabha 2029")
    st.progress(0.7)
    st.write("National Sentiment: Positive ↑")
    st.subheader("Key Issue Radar")
    issues = ["Inflation", "Employment", "Agriculture"]
    chart_data = pd.DataFrame(np.random.rand(3), index=issues, columns=["Salience"])
    st.line_chart(chart_data)

    if check_access(2):
        st.header("Constituency Deep-Dive")
        if 'selected_const' in st.session_state:
            const = st.session_state.selected_const
            st.subheader(f"Profile: {const['PC']}, {const['State']}")
            st.json(const["Demographics"])
            st.subheader("Anti-Incumbency Analysis")
            st.metric("Risk Score", const["Anti_Incumbency_Score"])
            new_candidate_strength = st.slider("New Candidate Strength", 0, 100, 50)
            simulated_prob = predict_win_prob(new_candidate_strength)
            st.write(f"Simulated Win Probability: {simulated_prob:.2f}%")
            st.subheader("Demographic Sentiment Matrix")
            matrix = pd.DataFrame(np.random.rand(4,4), columns=["Age 18-25", "26-40", "41-60", "60+"], index=["Male", "Female", "Urban", "Rural"])
            st.table(matrix)

        st.header("Deep Search")
        query = st.text_input("Natural Language Query", "Show ACs in Uttar Pradesh with anti-incumbency > 70")
        if query:
            filtered = constituencies[constituencies["Anti_Incumbency_Score"] > 70]
            st.table(filtered)
            st.write("Summary: High risk in selected areas.")

    if check_access(3):
        st.header("Campaign Management")
        st.subheader("Social Media Tracker")
        st.line_chart(np.random.rand(10))
        st.subheader("Field Operations")
        st.progress(0.5)
        st.write("Canvassing Progress: 50%")

    if check_access(4):
        st.header("Predictive Analytics")
        vote_share = st.slider("Adjust Campaign Spending", 0, 100, 50)
        prob = predict_win_prob(vote_share)
        st.metric("Projected Win Probability", f"{prob:.2f}%")

    st.header("Reports")
    if st.button("Generate PDF Report"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Bharat Chakra Report")
        c.drawString(100, 700, f"Win Probability: {np.random.randint(50,90)}%")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, "report.pdf", "application/pdf")
