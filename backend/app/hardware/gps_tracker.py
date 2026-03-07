"""
GPS Tracker Integration
This module handles GPS tracking for buses
"""

import requests
from typing import Optional, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GPSTracker:
    """GPS Tracker handler for buses"""
    
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        """
        Initialize GPS tracker
        
        Args:
            api_url: GPS tracking service API URL
            api_key: API key for authentication (if required)
        """
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def get_location(self, device_id: str) -> Optional[Dict]:
        """
        Get current location of a GPS device
        
        Args:
            device_id: GPS device ID
            
        Returns:
            Dictionary with location data (latitude, longitude, speed, heading, timestamp)
        """
        try:
            response = requests.get(
                f"{self.api_url}/devices/{device_id}/location",
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "speed": data.get("speed", 0),
                "heading": data.get("heading", 0),
                "timestamp": datetime.now()
            }
        except Exception as e:
            logger.error(f"Error getting GPS location: {e}")
            return None
    
    def get_all_locations(self) -> Dict[str, Dict]:
        """
        Get locations of all GPS devices
        
        Returns:
            Dictionary mapping device_id to location data
        """
        try:
            response = requests.get(
                f"{self.api_url}/devices/locations",
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting all GPS locations: {e}")
            return {}

# Example usage:
# tracker = GPSTracker(api_url="https://gps-api.example.com", api_key="your-api-key")
# location = tracker.get_location(device_id="bus-001")
# if location:
#     print(f"Bus location: {location['latitude']}, {location['longitude']}")





