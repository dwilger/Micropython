"""
MicroPython driver for Waveshare ED2208-GCA E-Paper Display
(2.13 inch, 250x122 pixels, Grayscale)

This driver provides support for the Waveshare ESP32-S3 PhotoPainter
with ED2208-GCA e-paper display module.

Author: MicroPython Community
License: MIT
"""

from micropython import const
from time import sleep_ms
import framebuf

# Display resolution
EPD_WIDTH = const(250)
EPD_HEIGHT = const(122)

# Display commands
DRIVER_OUTPUT_CONTROL = const(0x01)
BOOSTER_SOFT_START_CONTROL = const(0x0C)
GATE_SCAN_START_POSITION = const(0x0F)
DEEP_SLEEP_MODE = const(0x10)
DATA_ENTRY_MODE_SETTING = const(0x11)
SW_RESET = const(0x12)
TEMPERATURE_SENSOR_CONTROL = const(0x1A)
MASTER_ACTIVATION = const(0x20)
DISPLAY_UPDATE_CONTROL_1 = const(0x21)
DISPLAY_UPDATE_CONTROL_2 = const(0x22)
WRITE_RAM = const(0x24)
WRITE_VCOM_REGISTER = const(0x2C)
WRITE_LUT_REGISTER = const(0x32)
SET_DUMMY_LINE_PERIOD = const(0x3A)
SET_GATE_TIME = const(0x3B)
BORDER_WAVEFORM_CONTROL = const(0x3C)
SET_RAM_X_ADDRESS_START_END_POSITION = const(0x44)
SET_RAM_Y_ADDRESS_START_END_POSITION = const(0x45)
SET_RAM_X_ADDRESS_COUNTER = const(0x4E)
SET_RAM_Y_ADDRESS_COUNTER = const(0x4F)
TERMINATE_FRAME_READ_WRITE = const(0xFF)


class ED2208_GCA:
    """
    Driver for ED2208-GCA E-Paper Display
    
    This class provides methods to control and draw on the Waveshare
    ED2208-GCA grayscale e-paper display.
    """
    
    def __init__(self, spi, cs, dc, rst, busy):
        """
        Initialize the ED2208-GCA display driver.
        
        Args:
            spi: SPI bus object
            cs: Chip Select pin
            dc: Data/Command pin
            rst: Reset pin
            busy: Busy pin
        """
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        # Set initial pin values (pins should already be initialized)
        self.cs.value(1)
        self.dc.value(0)
        self.rst.value(0)
        
        # Create framebuffer (1 bit per pixel for black/white)
        self.buffer = bytearray(self.height * self.width // 8)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
        
        # Initialize the display
        self.init()
    
    def _spi_write(self, data):
        """Write data to SPI bus."""
        self.cs(0)
        self.spi.write(bytearray(data))
        self.cs(1)
    
    def _send_command(self, command):
        """Send command to display."""
        self.dc(0)
        self._spi_write([command])
    
    def _send_data(self, data):
        """Send data to display."""
        self.dc(1)
        if isinstance(data, int):
            self._spi_write([data])
        else:
            self._spi_write(data)
    
    def _wait_until_idle(self):
        """Wait until the display is idle (busy pin goes low)."""
        while self.busy.value() == 1:
            sleep_ms(10)
    
    def reset(self):
        """Hardware reset the display."""
        self.rst(1)
        sleep_ms(200)
        self.rst(0)
        sleep_ms(2)
        self.rst(1)
        sleep_ms(200)
    
    def init(self):
        """Initialize the display with default settings."""
        self.reset()
        self._wait_until_idle()
        
        # Software reset
        self._send_command(SW_RESET)
        self._wait_until_idle()
        
        # Driver output control
        self._send_command(DRIVER_OUTPUT_CONTROL)
        self._send_data((EPD_HEIGHT - 1) & 0xFF)
        self._send_data(((EPD_HEIGHT - 1) >> 8) & 0xFF)
        self._send_data(0x00)
        
        # Booster soft start control
        self._send_command(BOOSTER_SOFT_START_CONTROL)
        self._send_data(0xD7)
        self._send_data(0xD6)
        self._send_data(0x9D)
        
        # Write VCOM register
        self._send_command(WRITE_VCOM_REGISTER)
        self._send_data(0xA8)
        
        # Set dummy line period
        self._send_command(SET_DUMMY_LINE_PERIOD)
        self._send_data(0x1A)
        
        # Set gate time
        self._send_command(SET_GATE_TIME)
        self._send_data(0x08)
        
        # Data entry mode
        self._send_command(DATA_ENTRY_MODE_SETTING)
        self._send_data(0x03)
        
        # Set RAM address
        self._set_memory_area(0, 0, self.width - 1, self.height - 1)
        self._set_memory_pointer(0, 0)
        
        self._wait_until_idle()
    
    def _set_memory_area(self, x_start, y_start, x_end, y_end):
        """Set the memory area for drawing."""
        # Set RAM X address
        self._send_command(SET_RAM_X_ADDRESS_START_END_POSITION)
        self._send_data(x_start // 8)
        self._send_data(x_end // 8)
        
        # Set RAM Y address
        self._send_command(SET_RAM_Y_ADDRESS_START_END_POSITION)
        self._send_data(y_start & 0xFF)
        self._send_data((y_start >> 8) & 0xFF)
        self._send_data(y_end & 0xFF)
        self._send_data((y_end >> 8) & 0xFF)
    
    def _set_memory_pointer(self, x, y):
        """Set the memory pointer for drawing."""
        # Set RAM X address counter
        self._send_command(SET_RAM_X_ADDRESS_COUNTER)
        self._send_data(x // 8)
        
        # Set RAM Y address counter
        self._send_command(SET_RAM_Y_ADDRESS_COUNTER)
        self._send_data(y & 0xFF)
        self._send_data((y >> 8) & 0xFF)
    
    def clear(self, color=0xFF):
        """
        Clear the display.
        
        Args:
            color: Fill color (0xFF for white, 0x00 for black)
        """
        self._set_memory_area(0, 0, self.width - 1, self.height - 1)
        self._set_memory_pointer(0, 0)
        
        self._send_command(WRITE_RAM)
        # Send clear data in one buffer for efficiency
        clear_buffer = bytearray([color] * (self.width // 8 * self.height))
        self._send_data(clear_buffer)
        
        # Also clear framebuffer
        if color == 0xFF:
            self.fb.fill(0)
        else:
            self.fb.fill(1)
    
    def display(self):
        """Update the display with the framebuffer content."""
        self._set_memory_area(0, 0, self.width - 1, self.height - 1)
        self._set_memory_pointer(0, 0)
        
        self._send_command(WRITE_RAM)
        self._send_data(self.buffer)
        
        # Display update sequence
        self._send_command(DISPLAY_UPDATE_CONTROL_2)
        self._send_data(0xC7)
        self._send_command(MASTER_ACTIVATION)
        self._send_command(TERMINATE_FRAME_READ_WRITE)
        
        self._wait_until_idle()
    
    def sleep(self):
        """Put the display into deep sleep mode."""
        self._send_command(DEEP_SLEEP_MODE)
        self._send_data(0x01)
    
    # Drawing methods (using framebuffer)
    def fill(self, color):
        """Fill the entire display with a color."""
        self.fb.fill(color)
    
    def pixel(self, x, y, color):
        """Set a pixel at (x, y) to the specified color."""
        self.fb.pixel(x, y, color)
    
    def hline(self, x, y, w, color):
        """Draw a horizontal line."""
        self.fb.hline(x, y, w, color)
    
    def vline(self, x, y, h, color):
        """Draw a vertical line."""
        self.fb.vline(x, y, h, color)
    
    def line(self, x1, y1, x2, y2, color):
        """Draw a line from (x1, y1) to (x2, y2)."""
        self.fb.line(x1, y1, x2, y2, color)
    
    def rect(self, x, y, w, h, color, fill=False):
        """Draw a rectangle."""
        if fill:
            self.fb.fill_rect(x, y, w, h, color)
        else:
            self.fb.rect(x, y, w, h, color)
    
    def text(self, s, x, y, color=1):
        """Draw text at (x, y)."""
        self.fb.text(s, x, y, color)
    
    def blit(self, fbuf, x, y, key=-1, palette=None):
        """Blit another framebuffer to this one."""
        self.fb.blit(fbuf, x, y, key, palette)
