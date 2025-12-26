# Micropython
Repository for my Micropython Projects

## Projects

### Waveshare ESP32-S3 PhotoPainter Driver
Complete MicroPython driver for the Waveshare ESP32-S3 PhotoPainter board with ED2208-GCA e-paper display.

**Features:**
- Full support for 2.13" e-paper display (250x122 pixels)
- Hardware SPI communication
- Framebuffer-based graphics
- Text rendering and shape drawing
- Image display support
- Low power sleep mode
- Easy-to-use API

**Quick Start:**
```python
from waveshare_photopainter.config import create_display

epd = create_display()
epd.fill(0)
epd.text("Hello World!", 10, 10, 1)
epd.display()
epd.sleep()
```

For detailed documentation, see [waveshare_photopainter/README.md](waveshare_photopainter/README.md).

## License
MIT License - See LICENSE file for details.
