"""
MicroPython driver for Waveshare ED2208-GCA E-Paper Display
(2.13 inch, 250x122 pixels, Black and White)

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
    ED2208-GCA black and white e-paper display.
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


# AXP2101 PMIC Constants
AXP2101_ADDR = const(0x34)  # I2C address

# AXP2101 Register addresses
AXP2101_STATUS = const(0x00)
AXP2101_MODE_CHGSTATUS = const(0x01)
AXP2101_DATA_BUFFER0 = const(0x04)
AXP2101_VBUS_VOL_SET = const(0x16)
AXP2101_VSYS_VOL_SET = const(0x27)
AXP2101_POWER_ON_SOURCE = const(0x10)
AXP2101_POWER_OFF_EN = const(0x12)
AXP2101_DC_ONOFF_DVM = const(0x80)
AXP2101_LDO_ONOFF_SET = const(0x90)
AXP2101_ADC_CHANNEL_CONTROL = const(0x30)
AXP2101_TS_PIN_CONTROL = const(0x38)
AXP2101_IRQ_ENABLE1 = const(0x40)
AXP2101_IRQ_STATUS1 = const(0x48)


class AXP2101:
    """
    Driver for AXP2101 Power Management IC (PMIC)
    
    This class provides methods to initialize and control the AXP2101 PMIC
    used on the Waveshare ESP32-S3 PhotoPainter board for power management,
    battery charging, and voltage regulation.
    """
    
    def __init__(self, i2c, addr=AXP2101_ADDR):
        """
        Initialize the AXP2101 PMIC driver.
        
        Args:
            i2c: I2C bus object
            addr: I2C address of the AXP2101 (default: 0x34)
        """
        self.i2c = i2c
        self.addr = addr
        
        # Check if device is present
        try:
            self._read_reg(AXP2101_STATUS)
        except OSError:
            raise RuntimeError("AXP2101 not found at address 0x{:02X}".format(addr))
    
    def _read_reg(self, reg, nbytes=1):
        """Read one or more bytes from a register."""
        return self.i2c.readfrom_mem(self.addr, reg, nbytes)
    
    def _write_reg(self, reg, data):
        """Write one or more bytes to a register."""
        if isinstance(data, int):
            data = bytes([data])
        self.i2c.writeto_mem(self.addr, reg, data)
    
    def _set_bit(self, reg, bit):
        """Set a specific bit in a register."""
        val = self._read_reg(reg)[0]
        val |= (1 << bit)
        self._write_reg(reg, val)
    
    def _clear_bit(self, reg, bit):
        """Clear a specific bit in a register."""
        val = self._read_reg(reg)[0]
        val &= ~(1 << bit)
        self._write_reg(reg, val)
    
    def init(self):
        """
        Initialize the AXP2101 with default settings for ESP32-S3 PhotoPainter.
        
        This sets up power rails, charging parameters, and enables necessary
        LDOs for the display and other peripherals.
        """
        # Enable DCDC1 (3.3V for system)
        self._set_bit(AXP2101_DC_ONOFF_DVM, 0)
        
        # Enable DCDC2 (for ESP32-S3 core)
        self._set_bit(AXP2101_DC_ONOFF_DVM, 1)
        
        # Enable DCDC3 (for peripherals)
        self._set_bit(AXP2101_DC_ONOFF_DVM, 2)
        
        # Enable ALDO1 for e-paper display (typically 3.3V)
        self._set_bit(AXP2101_LDO_ONOFF_SET, 0)
        
        # Enable ALDO2 for additional peripherals
        self._set_bit(AXP2101_LDO_ONOFF_SET, 1)
        
        # Small delay for power stabilization
        sleep_ms(10)
    
    def enable_display_power(self):
        """Enable power rail for the e-paper display."""
        self._set_bit(AXP2101_LDO_ONOFF_SET, 0)
        sleep_ms(5)
    
    def disable_display_power(self):
        """Disable power rail for the e-paper display to save power."""
        self._clear_bit(AXP2101_LDO_ONOFF_SET, 0)
    
    def enable_dcdc1(self):
        """Enable DCDC1 (system power)."""
        self._set_bit(AXP2101_DC_ONOFF_DVM, 0)
    
    def disable_dcdc1(self):
        """Disable DCDC1 (system power)."""
        self._clear_bit(AXP2101_DC_ONOFF_DVM, 0)
    
    def enable_dcdc2(self):
        """Enable DCDC2 (ESP32 core power)."""
        self._set_bit(AXP2101_DC_ONOFF_DVM, 1)
    
    def disable_dcdc2(self):
        """Disable DCDC2 (ESP32 core power)."""
        self._clear_bit(AXP2101_DC_ONOFF_DVM, 1)
    
    def enable_dcdc3(self):
        """Enable DCDC3 (peripheral power)."""
        self._set_bit(AXP2101_DC_ONOFF_DVM, 2)
    
    def disable_dcdc3(self):
        """Disable DCDC3 (peripheral power)."""
        self._clear_bit(AXP2101_DC_ONOFF_DVM, 2)
    
    def get_status(self):
        """
        Get the current status of the PMIC.
        
        Returns:
            Status byte with power state information
        """
        return self._read_reg(AXP2101_STATUS)[0]
    
    def get_charging_status(self):
        """
        Get the battery charging status.
        
        Returns:
            Charging status byte
        """
        return self._read_reg(AXP2101_MODE_CHGSTATUS)[0]
    
    def is_charging(self):
        """
        Check if battery is currently charging.
        
        Returns:
            True if charging, False otherwise
        """
        status = self.get_charging_status()
        return (status & 0x0F) in [0x01, 0x02]  # Charging states
    
    def is_battery_present(self):
        """
        Check if battery is connected.
        
        Returns:
            True if battery is present, False otherwise
        """
        status = self.get_status()
        return bool(status & 0x08)
    
    def power_off(self):
        """
        Power off the system.
        
        Note: This will shut down the ESP32 board.
        """
        self._set_bit(AXP2101_POWER_OFF_EN, 0)
    
    def clear_irq(self):
        """Clear all interrupt flags."""
        # Clear IRQ status registers
        self._write_reg(AXP2101_IRQ_STATUS1, 0xFF)
        self._write_reg(AXP2101_IRQ_STATUS1 + 1, 0xFF)
    
    def enable_adc(self):
        """Enable ADC channels for voltage/current monitoring."""
        self._write_reg(AXP2101_ADC_CHANNEL_CONTROL, 0xFF)
    
    def disable_adc(self):
        """Disable ADC channels to save power."""
        self._write_reg(AXP2101_ADC_CHANNEL_CONTROL, 0x00)
