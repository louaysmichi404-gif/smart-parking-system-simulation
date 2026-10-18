
import random
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SmartPark | Control Center",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1120;
    color: #e5eaf4;
}

[data-testid="stSidebar"] {
    background: #101a2e;
    border-right: 1px solid #26334b;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

.hero {
    padding: 28px 30px;
    border: 1px solid #293954;
    border-radius: 20px;
    background: linear-gradient(120deg, #162742, #111a2d 70%, #123b3b);
    margin-bottom: 25px;
}

.eyebrow {
    color: #4adeb5;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero h1 {
    color: #f7faff;
    font-size: 34px;
    font-weight: 800;
    margin: 8px 0;
}

.hero p {
    color: #a9b8ce;
    margin-bottom: 0;
    font-size: 14px;
}

.kpi {
    background: #131e32;
    border: 1px solid #283650;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
}

.kpi-label {
    color: #9cacc3;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    color: #f6f8fc;
    font-size: 32px;
    font-weight: 800;
    margin: 9px 0 3px;
}

.kpi-note {
    color: #4adeb5;
    font-size: 12px;
}

.section-title {
    color: #f4f7fc;
    font-size: 21px;
    font-weight: 750;
    margin: 28px 0 14px;
}

.parking-card {
    background: #131e32;
    border: 1px solid #2a3851;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.parking-id {
    color: #f3f6fc;
    font-size: 20px;
    font-weight: 800;
}

.parking-type {
    color: #91a2bb;
    font-size: 12px;
    margin-top: 4px;
}

.status-free {
    display: inline-block;
    background: #103b32;
    color: #58e5b8;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}

.status-busy {
    display: inline-block;
    background: #452329;
    color: #ff9ba5;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 43px;
    font-weight: 650;
    border: 1px solid #334561;
}

div[data-testid="stMetric"] {
    background: #131e32;
    border: 1px solid #283650;
    padding: 15px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"] {
    color: #a9b8ce;
}

hr {
    border-color: #263650;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "parking" not in st.session_state:
    st.session_state.parking = {
        f"P{i}": False for i in range(1, 7)
    }

if "events" not in st.session_state:
    st.session_state.events = []

parking = st.session_state.parking


def record_event(space, event):
    st.session_state.events.insert(0, {
        "Time": datetime.now().strftime("%d %b %Y, %H:%M:%S"),
        "Space": space,
        "Event": event,
    })


def change_status(space, occupied, event):
    parking[space] = occupied
    record_event(space, event)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🅿️ SmartPark")
    st.caption("PARKING CONTROL CENTER")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Overview", "Parking Management", "Activity Log"],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.markdown("🟢 Simulation running")
    st.caption("Demo mode · No physical sensors")
    st.divider()
    st.caption("SmartPark Dashboard v1.0")


# ---------- CALCULATIONS ----------
total = len(parking)
occupied = sum(parking.values())
available = total - occupied
rate = occupied / total * 100 if total else 0

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">SMART MOBILITY · CONTROL CENTER</div>
    <h1>Parking Overview</h1>
    <p>Monitor space availability, manage simulated vehicle movements,
    and review parking activity from one dashboard.</p>
</div>
""", unsafe_allow_html=True)

if page == "Overview":
    st.markdown('<div class="section-title">Performance Overview</div>',
                unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    metrics = [
        (k1, "TOTAL SPACES", total, "Configured parking spaces"),
        (k2, "AVAILABLE", available, "Ready for vehicles"),
        (k3, "OCCUPIED", occupied, "Currently in use"),
        (k4, "OCCUPANCY RATE", f"{rate:.0f}%", "Current utilization"),
    ]

    for col, label, value, note in metrics:
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Live Parking Map</div>',
                unsafe_allow_html=True)
    st.caption("Status changes when you use the simulation controls.")

    cols = st.columns(3)
    for i, (space, is_occupied) in enumerate(parking.items()):
        badge = (
            '<span class="status-busy">● OCCUPIED</span>'
            if is_occupied else
            '<span class="status-free">● AVAILABLE</span>'
        )
        with cols[i % 3]:
            st.markdown(f"""
            <div class="parking-card">
                <div style="font-size:25px;margin-bottom:12px;">
                    {"🚗" if is_occupied else "🅿️"}
                </div>
                <div class="parking-id">{space}</div>
                <div class="parking-type">Standard parking bay</div>
                <div style="margin-top:16px;">{badge}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Occupancy Analytics</div>',
                unsafe_allow_html=True)

    chart_col, summary_col = st.columns([1.5, 1])

    with chart_col:
        chart_data = pd.DataFrame({
            "Status": ["Available", "Occupied"],
            "Spaces": [available, occupied],
        }).set_index("Status")
        st.bar_chart(chart_data, color="#4adeb5")

    with summary_col:
        st.markdown("#### Capacity utilization")
        st.progress(int(rate))
        st.write(f"**{rate:.0f}%** of total capacity is occupied.")
        st.caption(f"{available} of {total} spaces are currently available.")

elif page == "Parking Management":
    st.markdown('<div class="section-title">Manage Parking Spaces</div>',
                unsafe_allow_html=True)

    selected = st.selectbox("Select parking bay", list(parking.keys()))
    current = parking[selected]

    if current:
        st.error(f"{selected} is currently occupied.")
    else:
        st.success(f"{selected} is currently available.")

    a, b, c = st.columns(3)

    with a:
        if st.button("🚗 Register Arrival", use_container_width=True):
            if not parking[selected]:
                change_status(selected, True, "Vehicle arrived")
                st.rerun()
            else:
                st.warning("This space is already occupied.")

    with b:
        if st.button("🚙 Register Departure", use_container_width=True):
            if parking[selected]:
                change_status(selected, False, "Vehicle departed")
                st.rerun()
            else:
                st.warning("This space is already available.")

    with c:
        if st.button("🎲 Random Event", use_container_width=True):
            space = random.choice(list(parking.keys()))
            new_status = not parking[space]
            event = "Vehicle arrived" if new_status else "Vehicle departed"
            change_status(space, new_status, event)
            st.rerun()

    st.markdown('<div class="section-title">All Parking Bays</div>',
                unsafe_allow_html=True)

    for space, is_occupied in parking.items():
        left, middle, right = st.columns([1, 2, 1])
        left.write(f"**{space}**")
        middle.write("🔴 Occupied" if is_occupied else "🟢 Available")
        right.caption("In use" if is_occupied else "Free")

    if st.button("Reset All Spaces"):
        for space in parking:
            parking[space] = False
        record_event("ALL", "Parking lot reset")
        st.rerun()

elif page == "Activity Log":
    st.markdown('<div class="section-title">Parking Activity</div>',
                unsafe_allow_html=True)

    if st.session_state.events:
        st.dataframe(
            pd.DataFrame(st.session_state.events),
            use_container_width=True,
            hide_index=True,
        )

        csv = pd.DataFrame(st.session_state.events).to_csv(index=False)
        st.download_button(
            "⬇️ Export activity as CSV",
            data=csv,
            file_name="smartpark_activity.csv",
            mime="text/csv",
        )

        if st.button("Clear Activity Log"):
            st.session_state.events = []
            st.rerun()
    else:
        st.info("No activity recorded yet. Register an arrival or departure.")

# ---------- FOOTER ----------
st.divider()
st.caption(
    "SMARTPARK · Academic portfolio prototype · "
    "All parking occupancy data is simulated."
)
