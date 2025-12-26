"""
Image display example for Waveshare ESP32-S3 PhotoPainter

This example shows how to display images on the e-paper display.
Images should be converted to 1-bit (black and white) format.
"""

from machine import Pin, SPI
from drivers.ed2208_gca import ED2208_GCA
import framebuf
from time import sleep

# Pin configuration
SPI_SCK = 12
SPI_MOSI = 11
CS_PIN = 10
DC_PIN = 9
RST_PIN = 8
BUSY_PIN = 7

# Example 16x16 smiley face icon (1-bit bitmap)
SMILEY_ICON = bytearray([
    0b00000000, 0b00000000,
    0b00001111, 0b11110000,
    0b00111111, 0b11111100,
    0b01111111, 0b11111110,
    0b01110011, 0b11001110,
    0b11100011, 0b11000111,
    0b11100011, 0b11000111,
    0b11100011, 0b11000111,
    0b11100011, 0b11000111,
    0b11111111, 0b11111111,
    0b01111001, 0b10011110,
    0b01111001, 0b10011110,
    0b01111111, 0b11111110,
    0b00111111, 0b11111100,
    0b00001111, 0b11110000,
    0b00000000, 0b00000000,
])

def display_icon(epd, icon_data, width, height, x, y):
    """Display a bitmap icon on the display."""
    # Create a framebuffer for the icon
    icon_fb = framebuf.FrameBuffer(icon_data, width, height, framebuf.MONO_HLSB)
    
    # Blit the icon to the display
    epd.blit(icon_fb, x, y)

def create_simple_image():
    """Create a simple test pattern."""
    # Create a 50x50 checkerboard pattern
    width, height = 50, 50
    buffer = bytearray((width * height) // 8)
    fb = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HLSB)
    
    # Draw checkerboard
    for y in range(0, height, 10):
        for x in range(0, width, 10):
            if (x // 10 + y // 10) % 2 == 0:
                fb.fill_rect(x, y, 10, 10, 1)
    
    return buffer, width, height

def main():
    # Initialize hardware
    spi = SPI(1, baudrate=4000000, polarity=0, phase=0,
              sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    
    cs = Pin(CS_PIN, Pin.OUT)
    dc = Pin(DC_PIN, Pin.OUT)
    rst = Pin(RST_PIN, Pin.OUT)
    busy = Pin(BUSY_PIN, Pin.IN)
    
    # Initialize display
    print("Initializing display...")
    epd = ED2208_GCA(spi, cs, dc, rst, busy)
    
    # Clear and display title
    epd.fill(0)
    epd.text("Image Display", 10, 10, 1)
    epd.text("Demo", 10, 25, 1)
    
    # Display smiley icons at different positions
    print("Displaying icons...")
    display_icon(epd, SMILEY_ICON, 16, 16, 10, 50)
    display_icon(epd, SMILEY_ICON, 16, 16, 50, 50)
    display_icon(epd, SMILEY_ICON, 16, 16, 90, 50)
    display_icon(epd, SMILEY_ICON, 16, 16, 130, 50)
    
    epd.display()
    sleep(3)
    
    # Display checkerboard pattern
    print("Displaying pattern...")
    epd.fill(0)
    epd.text("Checkerboard:", 10, 10, 1)
    
    pattern_data, width, height = create_simple_image()
    pattern_fb = framebuf.FrameBuffer(pattern_data, width, height, framebuf.MONO_HLSB)
    epd.blit(pattern_fb, 100, 35)
    
    epd.display()
    sleep(3)
    
    # Sleep display
    epd.sleep()
    print("Done!")

if __name__ == "__main__":
    main()
