import os, sys
from PIL import Image
import numpy as np
import argparse

BYTE_SIZE = 6

def main():
    parser = argparse.ArgumentParser(description="Convert image to Oric bitmap data.")
    parser.add_argument("input_image", help="Input image file (e.g., example.png)")
    parser.add_argument("output_asm", help="Output ASM file (e.g., example.s)")
    parser.add_argument("-W", "--width", type=int, default=1, help="Character width in byte columns (default: 1)")
    parser.add_argument("-H", "--height", type=int, default=8, help="Character height in pixel rows (default: 8)")
    args = parser.parse_args()

    CHAR_WIDTH = args.width
    CHAR_HEIGHT = args.height
    BINARY_WIDTH = CHAR_WIDTH * BYTE_SIZE
    INPUT_IMAGE = args.input_image
    OUTPUT_ASM = args.output_asm

    img = np.asarray(Image.open(INPUT_IMAGE))

    height, width = img.shape
    scan_w, scan_h = width // (BINARY_WIDTH), height // CHAR_HEIGHT

    data: list[list[list[int]]] = []
    for j in range(scan_h):
        for i in range(scan_w):
            row = []
            for y in range(CHAR_HEIGHT):
                byte = 0
                for x in range(BINARY_WIDTH):
                    X = i * BINARY_WIDTH + x
                    Y = j * CHAR_HEIGHT + y
                    byte |= int(img[Y, X])
                    byte <<= 1
                byte >>= 1
                bytes_list = []
                for b in range(CHAR_WIDTH):
                    shift = (CHAR_WIDTH - 1 - b) * BYTE_SIZE
                    bytes_list.append((byte >> shift) & ((1 << BYTE_SIZE) - 1))
                row += [bytes_list]
            data += [row]

    res = ""
    for y in data:
        res += ".db "
        for x in y:
            for b in x:
                res += f"%{bin(b)[2:].rjust(8, '0')}, "
            res = res.rstrip(", ") + ";  "
            for b in x:
                for i in bin(b)[2:].rjust(6, '0'):
                    res += "." if i == '0' else "#"
                    res += " "
                res += " "
            res += "\n.db "
        res = res.rstrip(".db ")
        res += "\n"

    with open(OUTPUT_ASM, "w") as f:
        f.write(res)

if __name__ == "__main__":
    main()
