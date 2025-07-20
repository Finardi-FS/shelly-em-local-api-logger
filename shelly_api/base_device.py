# This file is a base class for Shelly Gen1 devices.
# It provides common methods to interact with the device's API.
# You can extend this class for specific device implementations like Shelly EM.
# Ensure you have the requests library installed: pip install requests

import requests

class ShellyDeviceGen1:
    def __init__(self, ip: str):
        self.ip = ip
        self.base_url = f"http://{self.ip}"

    def _get(self, endpoint: str):
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=3)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[Error] GET {endpoint}: {e}")
            return None

    def get_status(self):
        return self._get("/status")

    def get_settings(self):
        return self._get("/settings")

    def get_meter_info(self, index=0):
        status = self.get_status()
        return status.get("emeters", [])[index] if status else None