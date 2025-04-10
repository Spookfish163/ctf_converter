#!/usr/bin/env python3

import typing
from typing import List

class ConversionError(Exception):
    """Custom exception for conversion errors."""
    pass

class Converter:
    """
    Provides data conversion functionality for common cryptography types.
    Supported formats: decimal, text (characters), hex (hexadecimal), binary.
    """

    def load_data(self, filename: str) -> str:
        """Load data from a file."""
        try:
            with open(filename, "r") as data:
                return data.read()
        except IOError as e:
            raise ConversionError(f"Failed to read file {filename}: {e}")

    def _validate_decimal_range(self, decimal_list: List[int]) -> None:
        """Validate that decimal values are within the valid range (0-255)."""
        for decimal in decimal_list:
            if decimal < 0 or decimal > 255:
                raise ConversionError(f"Decimal value must be between 0-255: {decimal}")

    def decimal_to_text(self, decimal_list: List[int]) -> str:
        """Convert a list of decimal values to a text string."""
        self._validate_decimal_range(decimal_list)
        text = ""
        for i in decimal_list:
            text += self.d_to_t(i)
        return text

    def decimal_to_binary(self, decimal_list: List[int]) -> List[str]:
        """Convert a list of decimal values to binary strings."""
        self._validate_decimal_range(decimal_list)
        binary_list = []
        for i in decimal_list:
            binary_list.append(self.d_to_b(i))
        return binary_list

    def decimal_to_hex(self, decimal_list: List[int], as_single_value=False) -> str:
        """
        Convert a list of decimal values to a hex string.
        Args:
            as_single_value: If True, expects one number instead of a list
        """
        if as_single_value:
            return self.d_to_h(decimal_list)

        self._validate_decimal_range(decimal_list)
        hex_string = ""
        for i in decimal_list:
            hex_string += self.d_to_h(i)
        return hex_string

    def text_to_decimal(self, text: str) -> List[int]:
        """Convert a text string to a list of decimal values."""
        text = text.strip("\n")
        decimal_list = []
        for i in text:
            decimal_list.append(self.t_to_d(i))
        return decimal_list

    def text_to_hex(self, text: str) -> str:
        """Convert a text string to a hex string."""
        hex_string = ""
        for i in text:
            temp_decimal = self.t_to_d(i)
            hex_string += self.d_to_h(temp_decimal)
        return hex_string

    def text_to_binary(self, text: str) -> List[str]:
        """Convert a text string to a list of binary strings."""
        binary_list = []
        for i in text:
            decimal = self.t_to_d(i)
            binary_list.append(self.d_to_b(decimal))
        return binary_list

    def hex_to_decimal(self, hex_string: str, as_single_value=False) -> List[int]:
        """
        Convert a hex string to a list of decimal values.
        Args:
            as_single_value: If True, interprets the entire string as one large number
        """
        try:
            if hex_string.startswith("0x"):
                hex_string = hex_string[2:]

            if as_single_value:
                return int(hex_string, 16)

            hex_list = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            decimal_list = []
            for i in hex_list:
                decimal_list.append(int(i, 16))
            return decimal_list
        except ValueError:
            raise ConversionError(f"Invalid hex string: '{hex_string}'")

    def hex_to_text(self, hex_string: str) -> str:
        """Convert a hex string to a text string."""
        if not hex_string:
            return ""
        try:
            if hex_string.startswith("0x"):
                hex_string = hex_string[2:]
            hex_list = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            text = ""
            for i in hex_list:
                temp_decimal = int(i, 16)
                if temp_decimal < 0 or temp_decimal > 255:
                    raise ConversionError(f"Hex value must convert to 0-255: '{i}'")
                text += chr(temp_decimal)
            return text
        except ValueError:
            raise ConversionError(f"Invalid hex string: '{hex_string}'")

    def hex_to_binary(self, hex_string: str) -> List[str]:
        """Convert a hex string to a list of binary strings."""
        try:
            binary_list = []
            if hex_string.startswith("0x"):
                hex_string = hex_string[2:]
            hex_list = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            for hex_pair in hex_list:
                decimal = int(hex_pair, 16)
                if decimal < 0 or decimal > 255:
                    raise ConversionError(f"Hex value must convert to 0-255: '{hex_pair}'")
                binary_list.append(self.d_to_b(decimal))
            return binary_list
        except ValueError:
            raise ConversionError(f"Invalid hex string: '{hex_string}'")

    def binary_to_hex(self, binary_list: List[str]) -> str:
        """Convert a list of binary strings to a hex string."""
        for binary in binary_list:
            if len(binary) != 8 or not all(bit in "01" for bit in binary):
                raise ConversionError(f"Binary string must be 8 bits with only 0s and 1s: '{binary}'")
        hex_string = ""
        for binary in binary_list:
            decimal = self.b_to_d(binary)
            hex_string += self.d_to_h(decimal)
        return hex_string

    def binary_to_text(self, binary_list: List[str]) -> str:
        """Convert a list of binary strings to a text string."""
        for binary in binary_list:
            if len(binary) != 8 or not all(bit in "01" for bit in binary):
                raise ConversionError(f"Binary string must be 8 bits with only 0s and 1s: '{binary}'")
        text = ""
        for i in binary_list:
            decimal = self.b_to_d(i)
            text += self.d_to_t(decimal)
        return text

    def binary_to_decimal(self, binary_list: List[str]) -> List[int]:
        """Convert a list of binary strings to decimal values."""
        for binary in binary_list:
            if len(binary) != 8 or not all(bit in "01" for bit in binary):
                raise ConversionError(f"Binary string must be 8 bits with only 0s and 1s: '{binary}'")
        decimal_list = []
        for i in binary_list:
            decimal_list.append(self.b_to_d(i))
        return decimal_list

    def xor_text(self, text_a: str, text_b: str) -> str:
        """XOR two text strings together."""
        binary_list_a = self.text_to_binary(text_a)
        binary_list_b = self.text_to_binary(text_b)
        binary_list_c = []
        for i in range(min(len(binary_list_a), len(binary_list_b))):
            binary_list_c.append(self.xor_b(binary_list_a[i], binary_list_b[i]))
        return self.binary_to_text(binary_list_c)

    def xor_decimals(self, decimal_list_a: List[int], decimal_list_b: List[int]) -> List[int]:
        """XOR two lists of decimal values together."""
        self._validate_decimal_range(decimal_list_a)
        self._validate_decimal_range(decimal_list_b)
        xored_decs = []
        for i in range(min(len(decimal_list_a), len(decimal_list_b))):
            binary_a = self.d_to_b(decimal_list_a[i])
            binary_b = self.d_to_b(decimal_list_b[i])
            xored_binary = self.xor_b(binary_a, binary_b)
            xored_decs.append(self.b_to_d(xored_binary))
        return xored_decs

    def xor_b(self, binary_a: str, binary_b: str) -> str:
        """XOR two binary strings together."""
        binary_c = ""
        for i in range(8):
            x = int(binary_a[i]) ^ int(binary_b[i])
            binary_c += str(x)
        return binary_c

    def d_to_b(self, decimal: int) -> str:
        """Convert a decimal value to a binary string."""
        mult = 128
        binary_string = ""
        remaining = decimal

        for i in range(8):
            if remaining - mult >= 0:
                remaining -= mult
                binary_string += "1"
            else:
                binary_string += "0"
            mult = mult // 2
        return binary_string

    def d_to_t(self, decimal: int) -> str:
        """Convert a decimal value to a character."""
        return chr(decimal)

    def d_to_h(self, decimal: int) -> str:
        """Convert a decimal value to a hex string."""
        hex_char = hex(decimal)[2:]
        if len(hex_char) == 1:
            hex_char = "0" + hex_char
        return hex_char

    def b_to_d(self, binary_string: str) -> int:
        """Convert a binary string to a decimal value."""
        mult = 1
        decimal = 0
        for i in reversed(binary_string):
            if i == "1":
                decimal += mult
            mult *= 2
        return decimal

    def t_to_d(self, text: str) -> int:
        """Convert a character to its decimal value."""
        return ord(text)

    def h_to_d(self, hex_char: str) -> int:
        """Convert a hex string to a decimal value."""
        return int(hex_char, 16)
