"""
Hardware Configuration for Waveshare ESP32-S3 PhotoPainter

This module provides default pin configurations and hardware constants
for the Waveshare ESP32-S3 PhotoPainter board.

You can import these constants or override them with your own configuration.
"""

from machine import Pin

# Default SPI Pin Configuration
class DefaultPins:
    """Default pin assignments for Waveshare ESP32-S3 PhotoPainter"""
    
    # SPI pins
    SPI_SCK = 12    # SPI Clock
    SPI_MOSI = 11   # SPI Master Out Slave In
    SPI_MISO = 13   # SPI Master In Slave Out (if needed)
    
    # E-Paper Display Control Pins
    EPD_CS = 10     # Chip Select
    EPD_DC = 9      # Data/Command
    EPD_RST = 8     # Reset
    EPD_BUSY = 7    # Busy signal
    
    # SPI Configuration
    SPI_BAUDRATE = 4000000  # 4 MHz
    SPI_POLARITY = 0
    SPI_PHASE = 0
    SPI_BITS = 8
    SPI_FIRSTBIT = 0  # MSB first

# Display Specifications
class DisplaySpec:
    """ED2208-GCA Display Specifications"""
    
    WIDTH = 250
    HEIGHT = 122
    COLOR_DEPTH = 1  # 1-bit (black and white)
    
    # Display characteristics
    REFRESH_TIME_MS = 2000  # Typical refresh time in milliseconds
    FULL_REFRESH_CYCLES = 1000000  # Approximate max refresh cycles
    
    # Power consumption (typical values)
    ACTIVE_CURRENT_MA = 40  # During refresh
    SLEEP_CURRENT_UA = 1    # In deep sleep
    
    # Temperature range (Celsius)
    TEMP_MIN = 0
    TEMP_OPTIMAL = 25
    TEMP_MAX = 50

def get_default_spi(spi_id=1):
    """
    Get a configured SPI object with default settings.
    
    Args:
        spi_id: SPI bus ID (default: 1)
    
    Returns:
        Configured SPI object
    """
    from machine import SPI
    
    return SPI(
        spi_id,
        baudrate=DefaultPins.SPI_BAUDRATE,
        polarity=DefaultPins.SPI_POLARITY,
        phase=DefaultPins.SPI_PHASE,
        sck=Pin(DefaultPins.SPI_SCK),
        mosi=Pin(DefaultPins.SPI_MOSI)
    )

def get_default_pins():
    """
    Get default Pin objects for the display.
    
    Returns:
        Tuple of (cs, dc, rst, busy) Pin objects
    """
    cs = Pin(DefaultPins.EPD_CS, Pin.OUT)
    dc = Pin(DefaultPins.EPD_DC, Pin.OUT)
    rst = Pin(DefaultPins.EPD_RST, Pin.OUT)
    busy = Pin(DefaultPins.EPD_BUSY, Pin.IN)
    
    return cs, dc, rst, busy

def create_display():
    """
    Create and return an ED2208_GCA display object with default configuration.
    
    Returns:
        Initialized ED2208_GCA display object
    """
    from .drivers import ED2208_GCA
    
    spi = get_default_spi()
    cs, dc, rst, busy = get_default_pins()
    
    return ED2208_GCA(spi, cs, dc, rst, busy)

# Example usage
if __name__ == "__main__":
    # This shows how to use the configuration module
    print("Waveshare ESP32-S3 PhotoPainter Configuration")
    print(f"Display: {DisplaySpec.WIDTH}x{DisplaySpec.HEIGHT} pixels")
    print(f"SPI Pins: SCK={DefaultPins.SPI_SCK}, MOSI={DefaultPins.SPI_MOSI}")
    print(f"Control Pins: CS={DefaultPins.EPD_CS}, DC={DefaultPins.EPD_DC}, " +
          f"RST={DefaultPins.EPD_RST}, BUSY={DefaultPins.EPD_BUSY}")
