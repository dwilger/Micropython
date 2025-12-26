"""
Basic example for Waveshare ESP32-S3 PhotoPainter with ED2208-GCA display

This example demonstrates basic initialization and drawing on the e-paper display.
"""

from machine import Pin, SPI
from drivers.ed2208_gca import ED2208_GCA
from time import sleep

# Pin configuration for Waveshare ESP32-S3 PhotoPainter
# Adjust these pins according to your actual hardware configuration
SPI_SCK = 12   # SPI Clock
SPI_MOSI = 11  # SPI MOSI (Master Out Slave In)
CS_PIN = 10    # Chip Select
DC_PIN = 9     # Data/Command
RST_PIN = 8    # Reset
BUSY_PIN = 7   # Busy

def main():
    # Initialize SPI
    spi = SPI(1, baudrate=4000000, polarity=0, phase=0, 
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    
    # Initialize control pins
    cs = Pin(CS_PIN, Pin.OUT)
    dc = Pin(DC_PIN, Pin.OUT)
    rst = Pin(RST_PIN, Pin.OUT)
    busy = Pin(BUSY_PIN, Pin.IN)
    
    # Initialize display
    print("Initializing ED2208-GCA display...")
    epd = ED2208_GCA(spi, cs, dc, rst, busy)
    
    # Clear display
    print("Clearing display...")
    epd.clear(0xFF)
    epd.display()
    sleep(2)
    
    # Draw some text
    print("Drawing text...")
    epd.fill(0)
    epd.text("Hello, World!", 10, 10, 1)
    epd.text("Waveshare ESP32-S3", 10, 30, 1)
    epd.text("PhotoPainter", 10, 50, 1)
    epd.display()
    sleep(3)
    
    # Draw shapes
    print("Drawing shapes...")
    epd.fill(0)
    epd.rect(10, 10, 100, 50, 1)
    epd.rect(20, 20, 80, 30, 1, fill=True)
    epd.line(10, 70, 110, 70, 1)
    epd.hline(10, 80, 100, 1)
    epd.vline(120, 10, 80, 1)
    epd.display()
    sleep(3)
    
    # Put display to sleep
    print("Putting display to sleep...")
    epd.sleep()
    print("Done!")

if __name__ == "__main__":
    main()
