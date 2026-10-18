
import random
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SmartPark | Dashboard",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- PROFESSIONAL LIGHT THEME ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #f5f7fb;
    color: #172b4d;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(245,247,251,0.95);
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(110deg, #ffffff 0%, #edf8f7 100%);
    border: 1px solid #dce8ec;
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 26px;
    box-shadow: 0 4px 18px rgba(20, 45, 70, 0.04);
}

.eyebrow {
    color: #078779;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    color: #142d4e;
    font-size: 32px;
    font-weight: 800;
    margin: 8px 0;
}

.hero p {
    color: #63748b;
    font-size: 14px;
    margin: 0;
}

.section-title {
    color: #172b4d;
    font-size: 21px;
    font-weight: 750;
    margin: 26px 0 14px;
}

.kpi {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 20px;
    min-height: 126px;
    box-shadow: 0 3px 12px rgba(20, 45, 70, 0.035);
}

.kpi-label {
    color: #687b91;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .5px;
}

.kpi-value {
    color: #172b4d;
    font-size: 32px;
    font-weight: 800;
    margin: 10px 0 4px;
}

.kpi-note {
    color: #078779;
    font-size: 12px;
}

.parking-card {
    background: #ffffff;
    border: 1px solid #e0e7ef;
    border-radius: 15px;
    padding: 19px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(20, 45, 70, 0.035);
}

.parking-id {
    color: #172b4d;
    font-size: 20px;
    font-weight: 800;
}

.parking-type {
    color: #7b8ba0;
    font-size: 12px;
    margin-top: 5px;
}

.status-free {
    display: inline-block;
    background: #e5f7f0;
    color: #087b58;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}

.status-busy {
    display: inline-block;
    background: #fff0ee;
    color: #c34444;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 3px 12px rgba(20,45,70,0.025);
}

div[data-testid="stMetricLabel"] {
    color: #687b91;
}

div.stButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid #d6e0ea;
    background: #ffffff;
    color: #172b4d;
}

div.stButton > button:hover {
    border-color: #078779;
    color: #078779;
}

.stProgress > div > div > div > div {
    background-color: #078779;
}

hr {
    border-color: #e2e8f0;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

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


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🅿️ SmartPark")
    st.caption("PARKING MANAGEMENT")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Overview", "Parking Management", "Activity Log"],
    )

    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.success("Simulation active")
    st.caption("Demo mode · Virtual sensors")
    st.divider()
    st.caption("SmartPark Dashboard · v1.0")

# ---------------- STATISTICS ----------------

total = len(parking)
occupied = sum(parking.values())
available = total - occupied
rate = occupied / total * 100 if total else 0

# ---------------- HERO HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">SMART MOBILITY · CONTROL CENTER</div>
    <h1>Parking Overview</h1>
    <p>Monitor parking availability, simulate vehicle movements,
    and review parking activity from one central dashboard.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- OVERVIEW ----------------

if page == "Overview":

    st.markdown(
        '<div class="section-title">Performance Overview</div>',
        unsafe_allow_html=True,
    )

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

    st.markdown(
        '<div class="section-title">Parking Space Status</div>',
        unsafe_allow_html=True,
    )

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

    st.markdown(
        '<div class="section-title">Occupancy Analytics</div>',
        unsafe_allow_html=True,
    )

    chart_col, summary_col = st.columns([1.5, 1])

    with chart_col:
        chart_data = pd.DataFrame({
            "Status": ["Available", "Occupied"],
            "Spaces": [available, occupied],
        }).set_index("Status")

        st.bar_chart(chart_data, color="#078779")

    with summary_col:
        st.markdown("#### Capacity utilization")
        st.progress(int(rate))
        st.write(f"**{rate:.0f}%** of parking capacity is occupied.")
        st.caption(f"{available} of {total} spaces are available.")

# ---------------- PARKING MANAGEMENT ----------------

elif page == "Parking Management":

    st.markdown(
        '<div class="section-title">Manage Parking Spaces</div>',
        unsafe_allow_html=True,
    )

    selected = st.selectbox(
        "Select parking bay",
        list(parking.keys()),
    )

    if parking[selected]:
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
            event = (
                "Vehicle arrived"
                if new_status else "Vehicle departed"
            )
            change_status(space, new_status, event)
            st.rerun()

    st.markdown("#### All parking bays")

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

# ---------------- ACTIVITY LOG ----------------

elif page == "Activity Log":

    st.markdown(
        '<div class="section-title">Parking Activity</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.events:
        events_df = pd.DataFrame(st.session_state.events)

        st.dataframe(
            events_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Export activity as CSV",
            data=events_df.to_csv(index=False),
            file_name="smartpark_activity.csv",
            mime="text/csv",
        )

        if st.button("Clear Activity Log"):
            st.session_state.events = []
            st.rerun()
    else:
        st.info("No activity recorded yet. Register an arrival or departure.")

# ---------------- FOOTER ----------------

st.divider()
st.caption(
    "SMARTPARK · Academic portfolio prototype · "
    "All parking occupancy data is simulated."
)
