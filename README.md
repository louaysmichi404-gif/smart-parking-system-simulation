# Smart Parking System Simulation

## Overview
A Python-based IoT-style smart parking simulation developed using Google Colab. The project simulates parking sensors and monitors parking-space occupancy through a visual dashboard.

## Features
- Simulated parking sensors
- Real-time-style occupancy monitoring
- Automatic counting of available and occupied spaces
- Simulated vehicle arrivals and departures
- Color-coded dashboard for free and occupied parking spaces

## Technologies
- Python
- Matplotlib
- IPython Widgets
- Google Colab

## How It Works
Each parking space has a simulated sensor state:
- `0` = Free
- `1` = Occupied

The dashboard displays the status of each space. Users can simulate vehicle arrivals and departures to update the occupancy state.

## Project Status
Prototype completed in Google Colab. Sensor readings are simulated; no physical hardware is used.

## Future Improvements
- Add timestamps and sensor event logs
- Display occupancy statistics
- Store parking data in a CSV file
- Explore MQTT communication to simulate IoT messaging

## Author
Master's student in Electronics, Electrical Engineering and Automation (EEA), with a background in Mechatronics.
