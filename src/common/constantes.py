from enum import Enum

class Opcode(Enum):
    ADD = 0x01
    SUB = 0x02
    ZEROS = 0x03
    XOR = 0x04
    HALT = 0xFFFFFFFF
    MULT = 0x17
    DIV = 0x18

MASK_OPCODE = 0xFF000000
MASK_RA     = 0x00FF0000
MASK_RB     = 0x0000FF00
MASK_RC     = 0x000000FF