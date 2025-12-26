"""
Advanced graphics example for Waveshare ESP32-S3 PhotoPainter

This example demonstrates more advanced graphics capabilities including
drawing complex shapes and patterns.
"""

from machine import Pin, SPI
from drivers.ed2208_gca import ED2208_GCA
from time import sleep

# Pin configuration
SPI_SCK = 12
SPI_MOSI = 11
CS_PIN = 10
DC_PIN = 9
RST_PIN = 8
BUSY_PIN = 7

def draw_circle(epd, x0, y0, radius, color):
    """Draw a circle using midpoint circle algorithm."""
    x = radius
    y = 0
    err = 0
    
    while x >= y:
        epd.pixel(x0 + x, y0 + y, color)
        epd.pixel(x0 + y, y0 + x, color)
        epd.pixel(x0 - y, y0 + x, color)
        epd.pixel(x0 - x, y0 + y, color)
        epd.pixel(x0 - x, y0 - y, color)
        epd.pixel(x0 - y, y0 - x, color)
        epd.pixel(x0 + y, y0 - x, color)
        epd.pixel(x0 + x, y0 - y, color)
        
        if err <= 0:
            y += 1
            err += 2*y + 1
        
        if err > 0:
            x -= 1
            err -= 2*x + 1

def draw_pattern(epd):
    """Draw an interesting pattern."""
    # Clear display
    epd.fill(0)
    
    # Draw grid pattern
    for x in range(0, epd.width, 20):
        epd.vline(x, 0, epd.height, 1)
    
    for y in range(0, epd.height, 20):
        epd.hline(0, y, epd.width, 1)
    
    # Draw circles
    draw_circle(epd, 125, 61, 30, 1)
    draw_circle(epd, 125, 61, 20, 1)
    draw_circle(epd, 125, 61, 10, 1)
    
    epd.display()

def draw_animation_frames(epd):
    """Draw a series of frames showing movement."""
    for i in range(0, epd.width - 40, 20):
        epd.fill(0)
        epd.text("Moving ->", i, 50, 1)
        epd.rect(i, 40, 40, 20, 1)
        epd.display()
        sleep(1)

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
    
    # Draw pattern
    print("Drawing pattern...")
    draw_pattern(epd)
    sleep(3)
    
    # Draw animation
    print("Drawing animation...")
    draw_animation_frames(epd)
    
    # Final message
    epd.fill(0)
    epd.text("Demo Complete!", 50, 50, 1)
    epd.display()
    
    sleep(2)
    epd.sleep()
    print("Done!")

if __name__ == "__main__":
    main()
