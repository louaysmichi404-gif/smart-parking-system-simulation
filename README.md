
# SmartPark — Smart Parking Management System

A web-based parking management dashboard developed with Python and Streamlit.
The project simulates parking space occupancy and provides an interactive
interface for monitoring availability, managing vehicle movements, and
visualizing parking statistics.

## Overview

SmartPark demonstrates how a digital parking management system can help
monitor parking capacity and organize vehicle movements through a centralized
dashboard.

The application currently uses simulated parking data and does not require
physical sensors or specialized hardware.

## Features

- **Parking Space Monitoring:** View the status of six parking spaces.
- **Occupancy Statistics:** Display total, available, and occupied spaces.
- **Interactive Controls:** Simulate vehicle arrivals and departures.
- **Random Sensor Events:** Generate simulated parking status changes.
- **Data Visualization:** Display parking occupancy statistics in charts.
- **Activity Log:** Record vehicle movements and parking events.
- **CSV Export:** Download the activity history for further analysis.
- **Web Interface:** Access the dashboard through a browser.

## Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib-style data visualization through Streamlit charts
- Git and GitHub

## System Architecture

The current prototype follows this workflow:

1. Simulated parking events generate occupancy changes.
2. Python updates the parking space states.
3. Streamlit displays the current parking status and statistics.
4. Pandas organizes activity records for display and export.

## Installation

### Requirements

- Python 3.10 or later
- pip

### Run Locally

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/smart-parking-system-simulation.git
cd smart-parking-system-simulation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```

The application will open in your browser.

## Project Structure

```text
smart-parking-system-simulation/
├── app.py
├── requirements.txt
├── README.md
└── sensor_simulator.py
```

Note: `sensor_simulator.py` is a separate experimental file and is not
used by the current dashboard.

## Current Limitations

- Parking occupancy is simulated.
- No physical sensors are connected.
- MQTT integration is not currently enabled.
- Data is stored in the Streamlit session and is not a permanent database.

## Future Improvements

- Integrate ESP32 or Arduino parking sensors.
- Implement MQTT communication for live sensor updates.
- Add a database for persistent parking records.
- Introduce user authentication and access control.
- Extend the dashboard to support more parking spaces.
- Develop a physical or 3D parking lot visualization.

## Learning Objectives

This project explores the integration of Python programming, interactive
dashboards, event simulation, and data visualization in a smart mobility
application.

It is relevant to Mechatronics, Electronics, Embedded Systems, Industrial
Automation, and Internet of Things (IoT).

## Author

**Louay Smichi**

Master's student in Electronics, Electrical Engineering and Automation (EEA)

Interested in Mechatronics, Embedded Systems, Robotics, Industrial Automation,
and IoT.

---

*SmartPark is an educational portfolio prototype. All parking occupancy
readings are simulated.*
