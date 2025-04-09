# Data Converter

A Python utility for common cryptographic data format conversions. This tool simplifies working with different data representations frequently encountered in CTF challenges and cybersecurity work.

- Convert between decimal, text, hexadecimal, and binary formats
- Perform XOR operations on text strings and decimal lists

## Installation

```bash
# Clone the repository
git clone https://github.com/Spookfish163/ctf_converter.git
cd ctf_converter

```

## Usage Examples

```python
from ctf_converter import Converter

conv = Converter()

# Text conversions
hex_string = conv.text_to_hex("Hello, World!")  # "48656c6c6f2c20576f726c6421"
binary_list = conv.text_to_binary("ABC")  # ["01000001", "01000010", "01000011"]
decimal_list = conv.text_to_decimal("123")  # [49, 50, 51]

# Hex conversions
text = conv.hex_to_text("48656c6c6f")  # "Hello"
decimal_list = conv.hex_to_decimal("0xff")  # [255]
binary_list = conv.hex_to_binary("48656c6c6f")  # ["01001000", "01100101", ...]

# Binary conversions
text = conv.binary_to_text(["01001000", "01100101", "01101100", "01101100", "01101111"])  # "Hello"

# XOR operations
xor_result = conv.xor_text("secret", "key123")  # XOR two strings
```

## License

This project is licensed under the MIT License - see the [LICENSE section](https://opensource.org/licenses/MIT) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
