from manim import *
import numpy as np

__all__ = ["MBits"]


def convert_to_binary(bits, number):
    bit_max = max(len(bin(abs(number))) + 1, bits)
    upper_limit = 2 ** (bit_max - 1) - 1
    lower_limit = -2 ** (bit_max - 1)

    # 如果數字超出上下限，取最大bits
    if number < lower_limit or number > upper_limit:
        print(f"Warning: Number {number} is out of range for {bit_max}-bit two's complement representation. Taking the closest value.")
        number = max(min(number, upper_limit), lower_limit)

    # 如果是正數，直接返回二進制表示
    if number >= 0:
        binary_representation = bin(number)[2:].zfill(bit_max)
    else:
        # 如果是負數，計算補數
        positive_binary = bin(abs(number))[2:].zfill(bit_max)
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in positive_binary)

        # 進行加一操作
        inverted_decimal = int(inverted_binary, 2) + 1
        binary_representation = bin(inverted_decimal)[2:].zfill(bit_max)

    return binary_representation[0:bit_max - bits], binary_representation[bit_max - bits:len(binary_representation)]


class MBits(Polygon):
    overflow_text: VGroup
    binary_text: VGroup

    def __init__(
            self,
            color: ParsableManimColor = GRAY,
            bits: int = 1,
            number: int | None = None,
            show_overflow: bool = False,
            **kwargs,
    ):
        super().__init__(UR, UL, DL, DR, color=color, **kwargs)
        self.overflow, self.binary = convert_to_binary(bits, number)

        width = bits
        height = 1
        self.stretch_to_fit_width(width)
        self.stretch_to_fit_height(height)
        self._number = number
        self._bits = bits
        self.set_color = color

        v = self.get_vertices()
        self.sep = VGroup()

        for i in range(1, bits):
            self.sep.add(Line(v[1] + (i, 0, 0), v[1] + (i, 0, 0) + DOWN, color=color))

        if self.sep:
            self.add(self.sep)

        self.text = Text(show_overflow and self.overflow + self.binary or self.binary, color=color).align_to(self,
                                                                                                             RIGHT)

        for index, char in enumerate(self.text.submobjects.__reversed__()):
            char.move_to(v[3] - (index + 0.5, -0.5, 0))

        self.add(self.text)
        self.move_to(np.zeros(3, dtype=float))  # move to center

    @property
    def number(self):
        return self._number

    @property
    def bits(self):
        return self._bits
