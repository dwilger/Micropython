"""
Quick Start Example using Configuration Module

This example demonstrates the easiest way to get started with the
Waveshare ESP32-S3 PhotoPainter using the configuration helper.
"""

from waveshare_photopainter.config import create_display
from time import sleep

def main():
    # Create display with default configuration
    print("Initializing display with default configuration...")
    epd = create_display()
    
    # Clear the display
    print("Clearing display...")
    epd.clear(0xFF)
    epd.display()
    sleep(1)
    
    # Show welcome message
    print("Displaying welcome message...")
    epd.fill(0)
    epd.text("Quick Start!", 10, 10, 1)
    epd.text("Waveshare", 10, 30, 1)
    epd.text("ESP32-S3", 10, 50, 1)
    epd.text("PhotoPainter", 10, 70, 1)
    
    # Draw a border
    epd.rect(5, 5, 240, 112, 1)
    
    epd.display()
    sleep(3)
    
    # Show system info
    print("Displaying system info...")
    epd.fill(0)
    epd.text("Display Info:", 10, 10, 1)
    epd.text(f"Size: {epd.width}x{epd.height}", 10, 30, 1)
    epd.text("Type: E-Paper", 10, 50, 1)
    epd.text("Model: ED2208-GCA", 10, 70, 1)
    epd.display()
    sleep(3)
    
    # Put display to sleep
    print("Putting display to sleep...")
    epd.sleep()
    print("Done! Display is now in sleep mode.")

if __name__ == "__main__":
    main()
