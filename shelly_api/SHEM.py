# This file is a specific implementation for Shelly EM devices.
# It inherits from the base device class and provides methods to get power and energy data.
# Ensure you have the base_device.py in the same directory or adjust the import path accordingly.
# https://shelly-api-docs.shelly.cloud/gen1/#shelly-em-mqtt

from .base_device import ShellyDeviceGen1
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

class ShellyEM(ShellyDeviceGen1):
    def __init__(self, ip: str, db_path="shem_data.db"):
        super().__init__(ip)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                power REAL,
                total REAL,
                total_returned REAL,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

    def get_power_w(self, index = 0):
        """Get the instantaneous power in watts."""
        meter = self.get_meter_info(index)
        return meter.get("power") if meter else None

    def get_energy_consumed_wh(self, index=0):
        """Get the total energy consumed in watt-hours."""
        meter = self.get_meter_info(index)
        return meter.get("total") if meter else None    
    
    def get_energy_returned_wh(self, index=0):
        """Get the total energy returned in watt-hours."""
        meter = self.get_meter_info(index)
        return meter.get("total_returned") if meter else None
    
    def log_reading(self, index = 0):
        """Run a reading and save the results in the database."""
        meter = self.get_meter_info(index)
        if meter:
            power = meter.get("power")
            total = meter.get("total")
            total_returned = meter.get("total_returned")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO readings (power, total, total_returned, timestamp)
                VALUES (?, ?, ?, ?)
            """, (power, total, total_returned, timestamp))
            conn.commit()
            conn.close()
    
    def get_data_in_range(self, start_str: str, end_str: str):
        """Get historical data using date strings in 'YYYY-MM-DD HH:MM:SS' format."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM readings
            WHERE timestamp BETWEEN ? AND ?
        """, (start_str, end_str))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_power_plot(self, start_str: str, end_str: str):
        """Get a plot of power data in a specific date range."""


        data = self.get_data_in_range(start_str, end_str)
        if not data:
            print("No data found for the specified range.")
            return
        
        df = pd.DataFrame(data, columns=["id", "power", "total", "total_returned", "timestamp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["power"], label="Power (W)", color='blue')
        plt.title("Power Consumption Over Time")
        plt.xlabel("Time")
        plt.ylabel("Power (W)")
        plt.legend()
        plt.grid()
        plt.show()
    

