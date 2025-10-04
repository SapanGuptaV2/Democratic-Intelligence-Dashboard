import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import json

# Sample Data (Simulating ICPR datasets)
# GeoJSON for India map (simplified; use real GeoJSON in production)
india_geojson = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "properties": {"name": "Uttar Pradesh", "kpi": 65}, "geometry": {"type": "Polygon", "coordinates": [[[80,25],[82,26],[81,24]]]}},
        {"type": "Feature", "properties": {"name": "Maharashtra", "kpi": 50}, "geometry": {"type": "Polygon", "coordinates": [[[75,19],[77,20],[76,18]]]}},
        # Add more states/constituencies as needed
    ]
}

# Sample constituency data
constituencies = pd.DataFrame({
    "State": ["Uttar Pradesh", "Maharashtra"],
    "PC": ["Varanasi", "Mumbai North"],
    "Winning_Probability": [75, 60],
    "Anti_Incumbency_Score": [40, 55],
    "Sentiment_Index": [0.6, 0.4],
    "Demographics": [{"Caste": "General:50%, OBC:30%"}, {"Caste": "General:40%, SC:20%"}]
})

# Simulated AI Model for Predictions
def predict_win_prob(features):
    model = LogisticRegression()
    X = np.array([[1,2],[3,4]])  # Dummy training data
    y = np.array([0,1])
    model.fit(X, y)
    return model.predict_proba(np.array([features]))[0][1] * 100

# Authentication & RBAC
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = st.sidebar.selectbox("Role", ["National Admin", "Client", "Campaign Manager", "Field Manager", "Booth Worker"])
    if st.sidebar.button("Login"):
        # Simulate MFA (in production, integrate real MFA)
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

    # Role-based access control
    def check_access(level):
        roles = {"National Admin": 5, "Client": 4, "Campaign Manager": 3, "Field Manager": 2, "Booth Worker": 1}
        return roles.get(st.session_state.role, 0) >= level

    # Primary Dashboard
    st.title("Democratic Intelligence Dashboard")
    
    if check_access(3):  # Available to Manager and above
        # A. Interactive India Map
        st.header("Interactive India Map")
        kpi = st.selectbox("KPI for Coloring", ["Winning_Probability", "Anti_Incumbency_Score", "Sentiment_Index"])
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        folium.GeoJson(india_geojson, style_function=lambda feature: {
            'fillColor': 'green' if feature['properties']['kpi'] > 60 else 'red',
            'color': 'black',
            'weight': 1
        }).add_to(m)
        folium_static(m)
        
        # Filters and Drill-Down
        state = st.selectbox("Filter by State", constituencies["State"].unique())
        if st.button("Drill Down"):
            st.session_state.selected_const = constituencies[constituencies["State"] == state].iloc[0]

    # B. Political Weather Widgets
    st.header("Political Weather Overview")
    st.metric("Election Countdown", "30 days to Lok Sabha 2029")
    st.gauge = st.progress(0.7)  # Sentiment Gauge (simulate)
    st.write("National Sentiment: Positive ↑")
    
    issues = ["Inflation", "Employment", "Agriculture", "Security", "Education"]
    st.subheader("Key Issue Radar")
    st.bar_chart({"Issues": issues, "Salience": np.random.rand(5)})

    st.subheader("Alert Feed")
    st.write("Breaking: Sentiment shift in UP due to recent policy announcement.")

    # C. High-Level Analytics Tiles
    st.header("Analytics Tiles")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Seats to Win", "272/543")
    col2.metric("Swing Constituencies", "45")
    col3.metric("Resource Efficiency", "85%")
    col4.metric("Top Region", "Uttar Pradesh")

    if check_access(2):  # Field Manager and above
        # 3. Constituency Deep-Dive
        st.header("Constituency Deep-Dive")
        if 'selected_const' in st.session_state:
            const = st.session_state.selected_const
            st.subheader(f"Profile: {const['PC']}, {const['State']}")
            st.json(const["Demographics"])
            
            # Anti-Incumbency
            st.subheader("Anti-Incumbency Analysis")
            risk_score = const["Anti_Incumbency_Score"]
            st.metric("Risk Score", risk_score)
            st.write("Top Reasons: Poor Infrastructure, Low Visibility")
            
            # Simulator
            new_candidate_strength = st.slider("New Candidate Strength", 0, 100, 50)
            simulated_prob = predict_win_prob([new_candidate_strength, risk_score])
            st.write(f"Simulated Win Probability: {simulated_prob:.2f}%")
            
            # Sentiment Matrix
            st.subheader("Demographic Sentiment Matrix")
            matrix = pd.DataFrame(np.random.rand(4,4), columns=["Age 18-25", "26-40", "41-60", "60+"], index=["Male", "Female", "Urban", "Rural"])
            st.table(matrix)
        
        # D. Deep Search Bar
        st.header("Deep Search")
        query = st.text_input("Natural Language Query", "Show ACs in Uttar Pradesh with anti-incumbency > 70")
        if query:
            # Simulate parsing (extend to NLP in production)
            filtered = constituencies[constituencies["Anti_Incumbency_Score"] > 70]
            st.table(filtered)
            st.write("Summary: High risk in selected areas.")

    if check_access(3):  # Campaign Manager and above
        # 4. Campaign Management
        st.header("Campaign Management")
        st.subheader("Social Media Tracker")
        st.line_chart(np.random.rand(10))
        
        st.subheader("Field Operations")
        booth_progress = st.progress(0.5)
        st.write("Canvassing Progress: 50%")

    if check_access(4):  # Client and above
        # 5. Predictive Analytics
        st.header("Predictive Analytics")
        vote_share = st.slider("Adjust Campaign Spending", 0, 100, 50)
        prob = predict_win_prob([vote_share])
        st.metric("Projected Win Probability", f"{prob:.2f}%")

    # 7. Output & Reporting
    st.header("Reports")
    if st.button("Generate PDF Report"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Democratic Intelligence Report")
        c.drawString(100, 700, f"Win Probability: {np.random.randint(50,90)}%")
        c.save()
        buffer.seek(0)
        st.download_button("Download PDF", buffer, "report.pdf", "application/pdf")

    # Security Placeholder (The Sapan Protocol™ - simulate logging)
    st.write("All actions logged for audit.")

# Run with: streamlit run this_file.py