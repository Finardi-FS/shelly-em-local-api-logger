# Shelly EM API

This folder contains a Python library to interface with Shelly EM (Gen1) devices, read power/energy data, and log them to a local SQLite database.

## Features

- Read instantaneous power and total consumed/returned energy from a Shelly EM device.
- Log readings to a SQLite database.
- Retrieve historical data within a time range.
- Plot power data over time.

## Installation

Clone this repository and install the required dependencies:

```sh
pip install -r requirements.txt
```

## Example Usage (Jupyter Notebook)

Below is an example of how to use the library in a Jupyter notebook:

```python
from shelly_api import ShellyEM
from datetime import datetime

# Replace with your actual Shelly EM IP address
IP_SHELLY = "192.168.178.148"
shelly = ShellyEM(IP_SHELLY)

# Fetch and print instantaneous power and energy data
print("Shelly EM Power and Energy Data")
print("Power:\t\t", shelly.get_power_w())
print("Energy:\t\t", shelly.get_energy_consumed_wh())
print("Energy Returned:", shelly.get_energy_returned_wh())
```

### Logging Data in Background

To continuously log data, you should run the following code in a separate script or background process (not in the main notebook flow):

```python
import time
from datetime import datetime

t = 2  # seconds
print(f"Starting data logging every {t} seconds...")
try:
    while True:
        shelly.log_reading()
        print("Logged reading at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(t)
except KeyboardInterrupt:
    print("Manually interrupted.")
```

> **Note:**  
> This loop is intended to run in the background (for example, as a separate Python script or service) to continuously log readings.

### Fetching and Plotting Historical Data

```python
# Fetch historical data in a specific date range
shelly.get_data_in_range("2025-07-19 00:00:00", "2025-07-21 00:00:00")

# Plot power in a specific date range
shelly.get_power_plot("2025-07-20 17:15:00", "2025-07-20 18:20:00")
```

## Notes

- The SQLite database is created automatically (default: `shem_data.db`).
- Set the Shelly EM device IP according to your local network.
- You can change the database path by passing `db_path` to the `ShellyEM` constructor.

---

For more details on the Shelly  API: [Shelly Gen1 API Docs](https://shelly-api-docs.shelly.cloud/gen1/)
