
import random
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SmartPark | IoT Dashboard",
    page_icon="🚗",
    layout="wide",
)

# ---------- Styling ----------
st.markdown("""
<style>
.main {background-color: #f5f7fb;}
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "parking" not in st.session_state:
    st.session_state.parking = {
        "P1": False,
        "P2": True,
        "P3": False,
        "P4": True,
        "P5": False,
        "P6": True,
    }

if "events" not in st.session_state:
    st.session_state.events = []

def log_event(space, occupied, source="Simulation"):
    st.session_state.events.insert(0, {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Space": space,
        "Status": "OCCUPIED" if occupied else "FREE",
        "Source": source,
    })

# ---------- Header ----------
st.title("🚗 SmartPark")
st.caption("IoT Smart Parking Management — Simulation Dashboard")

parking = st.session_state.parking
total = len(parking)
occupied = sum(parking.values())
available = total - occupied
occupancy_rate = occupied / total * 100 if total else 0

# ---------- Metrics ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Spaces", total)
c2.metric("Available", available, delta="Free spaces")
c3.metric("Occupied", occupied)
c4.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")

st.divider()

# ---------- Parking lot ----------
left, right = st.columns([2, 1])

with left:
    st.subheader("🅿️ Parking Space Monitor")
    st.caption("Green = Free · Red = Occupied")

    cols = st.columns(3)
    for i, (space, is_occupied) in enumerate(parking.items()):
        with cols[i % 3]:
            status = "OCCUPIED 🔴" if is_occupied else "FREE 🟢"
            st.markdown(
                f"""
                <div style="
                    background:{'#fee2e2' if is_occupied else '#dcfce7'};
                    border:2px solid {'#ef4444' if is_occupied else '#22c55e'};
                    border-radius:12px;
                    padding:18px;
                    margin:6px 0;
                    text-align:center;
                ">
                    <h3 style="margin:0">{space}</h3>
                    <p style="margin:8px 0 0">{status}</p>
                    <small>Simulated sensor</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

with right:
    st.subheader("🎮 Simulation Controls")
    selected = st.selectbox("Choose parking space", list(parking.keys()))

    if st.button("🚘 Simulate Car Arrival", use_container_width=True):
        if parking[selected]:
            st.warning(f"{selected} is already occupied.")
        else:
            parking[selected] = True
            log_event(selected, True)
            st.rerun()

    if st.button("🚗 Simulate Car Departure", use_container_width=True):
        if not parking[selected]:
            st.warning(f"{selected} is already free.")
        else:
            parking[selected] = False
            log_event(selected, False)
            st.rerun()

    if st.button("🎲 Random Sensor Event", use_container_width=True):
        candidates = [
            s for s, state in parking.items()
            if not state
        ] or list(parking.keys())

        space = random.choice(candidates)
        parking[space] = not parking[space]
        log_event(space, parking[space])
        st.rerun()

    if st.button("🔄 Reset Parking", use_container_width=True):
        for space in parking:
            parking[space] = False
        log_event("ALL", False, "Reset")
        st.rerun()

# ---------- Chart ----------
st.divider()
st.subheader("📊 Occupancy Statistics")

chart_data = pd.DataFrame({
    "Status": ["Available", "Occupied"],
    "Spaces": [available, occupied],
}).set_index("Status")

st.bar_chart(chart_data)

# ---------- Event log ----------
st.subheader("📡 Sensor Event Log")

if st.session_state.events:
    st.dataframe(
        pd.DataFrame(st.session_state.events),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No events yet. Use the controls to simulate a car.")

st.caption(
    "Prototype: sensor readings are simulated. "
    "No physical sensors or live MQTT connection are used yet."
)
