"""
Waveshare ESP32-S3 PhotoPainter MicroPython Driver Package

This package provides a complete MicroPython driver for the Waveshare 
ESP32-S3 PhotoPainter board with ED2208-GCA e-paper display.

Main Components:
- ED2208_GCA: Driver for the 2.13" e-paper display
- AXP2101: Driver for the AXP2101 Power Management IC
- Examples: Demonstration scripts for various use cases
- Documentation: Complete API reference and guides

Usage:
    from waveshare_photopainter.drivers import ED2208_GCA, AXP2101
    from machine import Pin, SPI, I2C
    
    # Initialize PMIC
    i2c = I2C(0, scl=Pin(18), sda=Pin(17))
    pmic = AXP2101(i2c)
    pmic.init()
    
    # Initialize display
    spi = SPI(1, baudrate=4000000, polarity=0, phase=0,
              sck=Pin(12), mosi=Pin(11))
    epd = ED2208_GCA(spi, Pin(10), Pin(9), Pin(8), Pin(7))
    
    epd.fill(0)
    epd.text("Hello World!", 10, 10, 1)
    epd.display()

For more examples, see the examples/ directory.
For complete documentation, see README.md.
"""

__version__ = '1.0.0'
__author__ = 'MicroPython Community'
__license__ = 'MIT'

# Make the main drivers easily accessible
from .drivers import ED2208_GCA, AXP2101

__all__ = ['ED2208_GCA', 'AXP2101']
