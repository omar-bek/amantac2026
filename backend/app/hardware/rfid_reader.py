"""
RFID Reader Integration
This module handles communication with RFID readers
"""

import serial
import time
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)

class RFIDReader:
    """RFID Reader handler"""
    
    def __init__(self, port: str, baudrate: int = 9600):
        """
        Initialize RFID reader
        
        Args:
            port: Serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate: Serial communication baudrate
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection: Optional[serial.Serial] = None
        self.callback: Optional[Callable] = None
    
    def connect(self):
        """Connect to RFID reader"""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            logger.info(f"Connected to RFID reader on {self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to RFID reader: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from RFID reader"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            logger.info("Disconnected from RFID reader")
    
    def read_tag(self) -> Optional[str]:
        """
        Read RFID tag ID
        
        Returns:
            Tag ID as string, or None if no tag detected
        """
        if not self.serial_connection or not self.serial_connection.is_open:
            return None
        
        try:
            if self.serial_connection.in_waiting > 0:
                data = self.serial_connection.readline().decode('utf-8').strip()
                return data
        except Exception as e:
            logger.error(f"Error reading RFID tag: {e}")
        
        return None
    
    def set_callback(self, callback: Callable[[str], None]):
        """
        Set callback function for tag detection
        
        Args:
            callback: Function to call when tag is detected (receives tag_id)
        """
        self.callback = callback
    
    def start_listening(self):
        """Start listening for RFID tags in a loop"""
        if not self.serial_connection or not self.serial_connection.is_open:
            logger.error("RFID reader not connected")
            return
        
        logger.info("Started listening for RFID tags...")
        while True:
            tag_id = self.read_tag()
            if tag_id and self.callback:
                self.callback(tag_id)
            time.sleep(0.1)

# Example usage:
# reader = RFIDReader(port='COM3')
# reader.connect()
# 
# def on_tag_detected(tag_id):
#     print(f"Tag detected: {tag_id}")
#     # Process tag detection (log attendance, etc.)
# 
# reader.set_callback(on_tag_detected)
# reader.start_listening()





