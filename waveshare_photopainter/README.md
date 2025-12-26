# Waveshare ESP32-S3 PhotoPainter Driver

MicroPython driver for the Waveshare ESP32-S3 PhotoPainter with ED2208-GCA e-paper display.

## Features

- Full support for ED2208-GCA 2.13" e-paper display (250x122 pixels)
- Hardware SPI communication
- Framebuffer-based drawing operations
- Low power consumption with deep sleep mode
- Drawing primitives (lines, rectangles, circles)
- Text rendering
- Image display support

## Hardware Specifications

### ED2208-GCA Display
- **Resolution**: 250 x 122 pixels
- **Display Size**: 2.13 inches
- **Color**: Black and White (1-bit)
- **Interface**: SPI
- **Viewing Angle**: >170°
- **Refresh Time**: ~2 seconds

### Pin Configuration

The driver requires the following connections:

| Pin Function | ESP32-S3 Pin | Description |
|--------------|--------------|-------------|
| SPI_SCK      | GPIO 12      | SPI Clock |
| SPI_MOSI     | GPIO 11      | SPI Data Out |
| CS           | GPIO 10      | Chip Select |
| DC           | GPIO 9       | Data/Command |
| RST          | GPIO 8       | Reset |
| BUSY         | GPIO 7       | Busy Signal |

**Note**: Pin numbers may vary depending on your specific board configuration. Adjust them in the example code accordingly.

## Installation

1. Copy the `waveshare_photopainter` directory to your MicroPython device
2. Ensure your MicroPython firmware supports the `framebuf` module

### File Structure
```
waveshare_photopainter/
├── drivers/
│   ├── __init__.py
│   └── ed2208_gca.py       # Main display driver
└── examples/
    ├── basic_demo.py         # Basic usage example
    ├── advanced_graphics.py  # Advanced graphics demo
    └── image_display.py      # Image display example
```

## Quick Start

### Basic Usage

```python
from machine import Pin, SPI
from drivers.ed2208_gca import ED2208_GCA

# Initialize SPI
spi = SPI(1, baudrate=4000000, polarity=0, phase=0,
          sck=Pin(12), mosi=Pin(11))

# Initialize control pins
cs = Pin(10, Pin.OUT)
dc = Pin(9, Pin.OUT)
rst = Pin(8, Pin.OUT)
busy = Pin(7, Pin.IN)

# Initialize display
epd = ED2208_GCA(spi, cs, dc, rst, busy)

# Clear display
epd.clear(0xFF)
epd.display()

# Draw text
epd.fill(0)
epd.text("Hello World!", 10, 10, 1)
epd.display()

# Put display to sleep to save power
epd.sleep()
```

## API Reference

### ED2208_GCA Class

#### Initialization

```python
ED2208_GCA(spi, cs, dc, rst, busy)
```

**Parameters:**
- `spi`: SPI bus object
- `cs`: Chip Select pin (Pin object)
- `dc`: Data/Command pin (Pin object)
- `rst`: Reset pin (Pin object)
- `busy`: Busy pin (Pin object)

#### Display Control Methods

##### `clear(color=0xFF)`
Clear the entire display.
- `color`: Fill color (0xFF for white, 0x00 for black)

##### `display()`
Update the display with the current framebuffer content. This method triggers the e-paper refresh cycle.

##### `sleep()`
Put the display into deep sleep mode to save power.

##### `init()`
Initialize or re-initialize the display. Called automatically during object creation.

#### Drawing Methods

All drawing operations work on the internal framebuffer. Call `display()` to update the physical screen.

##### `fill(color)`
Fill the entire framebuffer with a color.
- `color`: 0 for white, 1 for black

##### `pixel(x, y, color)`
Set a single pixel.
- `x`, `y`: Pixel coordinates
- `color`: 0 for white, 1 for black

##### `hline(x, y, w, color)`
Draw a horizontal line.
- `x`, `y`: Starting position
- `w`: Line width in pixels
- `color`: 0 for white, 1 for black

##### `vline(x, y, h, color)`
Draw a vertical line.
- `x`, `y`: Starting position
- `h`: Line height in pixels
- `color`: 0 for white, 1 for black

##### `line(x1, y1, x2, y2, color)`
Draw a line between two points.
- `x1`, `y1`: Start coordinates
- `x2`, `y2`: End coordinates
- `color`: 0 for white, 1 for black

##### `rect(x, y, w, h, color, fill=False)`
Draw a rectangle.
- `x`, `y`: Top-left corner position
- `w`, `h`: Width and height
- `color`: 0 for white, 1 for black
- `fill`: If True, fill the rectangle; if False, draw outline only

##### `text(s, x, y, color=1)`
Draw text using the built-in 8x8 font.
- `s`: String to display
- `x`, `y`: Text position
- `color`: 0 for white, 1 for black

##### `blit(fbuf, x, y, key=-1, palette=None)`
Blit (copy) another framebuffer onto this one.
- `fbuf`: Source framebuffer
- `x`, `y`: Destination position
- `key`: Transparent color key (optional)
- `palette`: Color palette (optional)

## Examples

### Example 1: Display Text and Shapes

```python
from machine import Pin, SPI
from drivers.ed2208_gca import ED2208_GCA
from time import sleep

# Setup (use your pin configuration)
spi = SPI(1, baudrate=4000000, polarity=0, phase=0,
          sck=Pin(12), mosi=Pin(11))
epd = ED2208_GCA(spi, Pin(10), Pin(9), Pin(8), Pin(7))

# Clear and draw
epd.fill(0)
epd.text("ESP32-S3", 10, 10, 1)
epd.rect(10, 30, 100, 50, 1)
epd.line(10, 90, 110, 90, 1)
epd.display()

sleep(5)
epd.sleep()
```

### Example 2: Display an Image

```python
import framebuf

# Create or load image data (1-bit bitmap)
img_data = bytearray([...])  # Your image data here
img_width, img_height = 64, 64

# Create framebuffer for the image
img_fb = framebuf.FrameBuffer(img_data, img_width, img_height, 
                              framebuf.MONO_HLSB)

# Display the image
epd.fill(0)
epd.blit(img_fb, 50, 30)
epd.display()
```

### Example 3: Animation

```python
# Simple animation moving a box across the screen
for x in range(0, 200, 10):
    epd.fill(0)
    epd.rect(x, 50, 30, 20, 1, fill=True)
    epd.text("Moving...", x, 30, 1)
    epd.display()
    sleep(0.5)
```

## Power Consumption

E-paper displays are known for their ultra-low power consumption:
- **Active**: ~40mA (during refresh)
- **Sleep**: <1µA (deep sleep mode)
- **Display retention**: 0W (image persists without power)

Always call `epd.sleep()` when you're done updating the display to minimize power consumption.

## Tips and Best Practices

1. **Minimize Refreshes**: E-paper displays have limited refresh cycles (typically 1,000,000+). Avoid unnecessary refreshes.

2. **Use Sleep Mode**: Always put the display to sleep when not actively updating it.

3. **Batch Updates**: Draw all your content to the framebuffer first, then call `display()` once.

4. **Avoid Rapid Updates**: E-paper displays need time to refresh (1-2 seconds). Don't try to update too quickly.

5. **Image Preparation**: For best results, convert images to 1-bit (black and white) format before displaying.

6. **Temperature**: E-paper displays work best at room temperature (15-25°C). Extreme temperatures affect refresh speed.

## Troubleshooting

### Display Not Responding
- Check all pin connections
- Verify SPI bus is properly initialized
- Ensure power supply is stable (3.3V)
- Try calling `epd.reset()` manually

### Display Shows Ghosting
- This is normal for e-paper displays
- Clear the display with `epd.clear(0xFF)` followed by `epd.display()`
- Some ghosting is inherent to e-paper technology

### Slow Updates
- E-paper displays inherently take 1-2 seconds to refresh
- This is normal behavior and cannot be significantly improved
- Temperature affects refresh speed

### Image Appears Corrupted
- Verify image dimensions match your display (250x122)
- Check that image format is 1-bit (MONO_HLSB)
- Ensure framebuffer is properly aligned

## Technical Details

### Display Commands

The driver implements the following key e-paper display commands:
- Driver Output Control
- Booster Soft Start
- VCOM Register Setting
- Data Entry Mode
- RAM Address Setting
- Display Update Control
- Deep Sleep Mode

### Memory Layout

The display uses a horizontal layout where:
- Width: 250 pixels (32 bytes, using 31 bytes + 2 pixels)
- Height: 122 pixels
- Total buffer size: 3,813 bytes (250 * 122 / 8)

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## References

- [Waveshare ESP32-S3 PhotoPainter](https://www.waveshare.com/wiki/ESP32-S3-PhotoPainter)
- [MicroPython Documentation](https://docs.micropython.org/)
- [E-Paper Display Technology](https://en.wikipedia.org/wiki/Electronic_paper)

## Support

For issues and questions:
- Open an issue on GitHub
- Check Waveshare's official documentation
- Visit MicroPython forums

---

**Version**: 1.0.0  
**Last Updated**: December 2024
