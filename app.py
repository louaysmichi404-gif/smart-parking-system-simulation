
import random
from datetime import datetime

import pandas as pd
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="SmartPark Dashboard",
    page_icon="🅿️",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "parking" not in st.session_state:
    st.session_state.parking = {
        f"P{i}": False for i in range(1, 7)
    }

if "events" not in st.session_state:
    st.session_state.events = []

parking = st.session_state.parking


# ---------------- HELPER FUNCTION ----------------

def record_event(space, event):
    st.session_state.events.insert(0, {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Parking Space": space,
        "Event": event,
        "Source": "Simulation"
    })


def set_parking_status(space, occupied, event_name):
    parking[space] = occupied
    record_event(space, event_name)


# ---------------- HEADER ----------------

st.title("🅿️ SmartPark")
st.subheader("Intelligent Parking Management System")
st.write(
    "Monitor parking spaces, simulate vehicle movements, "
    "and view parking availability in real time within this demo."
)

st.divider()

# ---------------- STATISTICS ----------------

total = len(parking)
occupied = sum(parking.values())
available = total - occupied
occupancy_rate = (occupied / total * 100) if total else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Spaces", total)
c2.metric("Available Spaces", available)
c3.metric("Occupied Spaces", occupied)
c4.metric("Occupancy Rate", f"{occupancy_rate:.0f}%")

st.divider()

# ---------------- PARKING SPACE CARDS ----------------

st.header("🚘 Parking Lot Status")

columns = st.columns(3)

for index, (space, is_occupied) in enumerate(parking.items()):
    with columns[index % 3]:
        if is_occupied:
            st.error(f"🚗 {space} — OCCUPIED")
            st.caption("This parking space is in use.")
        else:
            st.success(f"🅿️ {space} — AVAILABLE")
            st.caption("This parking space is free.")

st.divider()

# ---------------- CONTROLS ----------------

st.header("🎮 Parking Controls")

selected_space = st.selectbox(
    "Choose a parking space",
    list(parking.keys())
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚗 Simulate Arrival", use_container_width=True):
        if not parking[selected_space]:
            set_parking_status(
                selected_space, True, "Vehicle arrived"
            )
            st.success(f"{selected_space} is now occupied.")
        else:
            st.warning(f"{selected_space} is already occupied.")
        st.rerun()

with col2:
    if st.button("🚙 Simulate Departure", use_container_width=True):
        if parking[selected_space]:
            set_parking_status(
                selected_space, False, "Vehicle departed"
            )
            st.success(f"{selected_space} is now available.")
        else:
            st.warning(f"{selected_space} is already available.")
        st.rerun()

with col3:
    if st.button("🎲 Random Sensor Event", use_container_width=True):
        space = random.choice(list(parking.keys()))
        new_status = random.choice([True, False])

        event = "Vehicle detected" if new_status else "Space detected free"

        set_parking_status(space, new_status, event)
        st.info(f"{space}: {'OCCUPIED' if new_status else 'AVAILABLE'}")
        st.rerun()

col4, col5 = st.columns(2)

with col4:
    if st.button("🔄 Reset Parking Lot", use_container_width=True):
        for space in parking:
            parking[space] = False

        record_event("All spaces", "Parking lot reset")
        st.rerun()

with col5:
    if st.button("🗑️ Clear Event Log", use_container_width=True):
        st.session_state.events = []
        st.rerun()

st.divider()

# ---------------- CHART ----------------

st.header("📊 Parking Statistics")

chart_data = pd.DataFrame({
    "Status": ["Available", "Occupied"],
    "Number of Spaces": [available, occupied]
}).set_index("Status")

st.bar_chart(chart_data)

# ---------------- EVENT LOG ----------------

st.header("📡 Parking Event Log")

if st.session_state.events:
    events_df = pd.DataFrame(st.session_state.events)
    st.dataframe(
        events_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No events yet. Use the controls to simulate a vehicle.")

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "SmartPark Prototype | Python + Streamlit | "
    "Parking sensors and vehicle movements are simulated. "
    "No MQTT connection or physical sensors are used."
)
