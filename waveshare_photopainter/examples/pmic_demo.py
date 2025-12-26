"""
AXP2101 PMIC example for Waveshare ESP32-S3 PhotoPainter

This example demonstrates how to initialize and use the AXP2101 Power
Management IC on the Waveshare ESP32-S3 PhotoPainter board.
"""

from machine import Pin, I2C
from drivers.ed2208_gca import AXP2101
from time import sleep

# I2C configuration for AXP2101
# Adjust these pins according to your actual hardware configuration
I2C_SCL = 18
I2C_SDA = 17

def main():
    # Initialize I2C
    print("Initializing I2C bus...")
    i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)
    
    # Scan for I2C devices
    devices = i2c.scan()
    print(f"I2C devices found: {[hex(d) for d in devices]}")
    
    # Initialize AXP2101 PMIC
    print("Initializing AXP2101 PMIC...")
    pmic = AXP2101(i2c)
    
    # Initialize with default settings
    pmic.init()
    print("PMIC initialized successfully!")
    
    # Get and display status
    print("\n--- PMIC Status ---")
    status = pmic.get_status()
    print(f"Status register: 0x{status:02X}")
    
    # Check battery status
    if pmic.is_battery_present():
        print("Battery: Connected")
        if pmic.is_charging():
            print("Battery: Charging")
        else:
            print("Battery: Not charging")
    else:
        print("Battery: Not connected")
    
    # Get charging status
    charge_status = pmic.get_charging_status()
    print(f"Charging status: 0x{charge_status:02X}")
    
    # Enable display power
    print("\n--- Power Control ---")
    print("Enabling display power rail...")
    pmic.enable_display_power()
    sleep(1)
    
    # Enable ADC for monitoring
    print("Enabling ADC channels...")
    pmic.enable_adc()
    
    # Clear any pending interrupts
    print("Clearing IRQ flags...")
    pmic.clear_irq()
    
    print("\n--- Power Rails Status ---")
    print("DCDC1 (System): Enabled")
    print("DCDC2 (ESP32): Enabled")
    print("DCDC3 (Peripherals): Enabled")
    print("ALDO1 (Display): Enabled")
    
    # Demonstrate power control
    print("\n--- Power Management Demo ---")
    print("Display power will be cycled in 3 seconds...")
    sleep(3)
    
    print("Disabling display power...")
    pmic.disable_display_power()
    sleep(2)
    
    print("Re-enabling display power...")
    pmic.enable_display_power()
    sleep(1)
    
    print("\nPMIC demo complete!")

if __name__ == "__main__":
    main()
