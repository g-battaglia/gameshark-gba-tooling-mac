#!/usr/bin/env python3
"""Decrypt and classify AR V3 code pairs.

Usage:
    python3 verify.py "ENCADDR ENCVAL" ["ENCADDR ENCVAL" ...]

Each argument is a pair "aaaaaaaa bbbbbbbb" (hex). Prints the decrypted
address/value and flags hook codes (c4......) and game-ID lines (value 001dc0de).

Requires arcrypt.py in the parent directory.
"""
import os
import sys
import struct

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import arcrypt

GAME_CODES = {
    0x45565841: "AXVE  (Pokémon Ruby    USA)",
    0x45505841: "AXPE  (Pokémon Sapphire USA)",
    0x50565841: "AXVP  (Pokémon Ruby    EUR)",
    0x50505841: "AXPP  (Pokémon Sapphire EUR)",
    0x4A565841: "AXVJ  (Pokémon Ruby    JPN)",
    0x4A505841: "AXPJ  (Pokémon Sapphire JPN)",
    0x45475042: "BPGE  (Pokémon FireRed EUR, seen on device)",
    0x45445941: "AYDE  (Dungeon Dice Monsters, seen on device)",
}


def classify(a, v):
    tags = []
    if v == 0x001DC0DE:
        gid = GAME_CODES.get(a, "unknown game code %08x" % a)
        tags.append("GAME-ID -> %s" % gid)
    hi = a & 0xFF000000
    if hi == 0xC4000000:
        tags.append("HOOK c4  rom_addr=0x%06x" % (a & 0x00FFFFFF))
    elif hi in (0x00000000, 0x02000000, 0x03000000):
        tags.append("write-type (hi=%02x)" % (hi >> 24))
    return tags


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    seeds = arcrypt.seed(0)
    for arg in sys.argv[1:]:
        parts = arg.split()
        if len(parts) != 2:
            print("  ignoring malformed: %r" % arg)
            continue
        enc = (int(parts[0], 16), int(parts[1], 16))
        a, v = arcrypt.decrypt(seeds, enc)
        tags = " | ".join(classify(a, v)) or "(no recognized pattern)"
        print("  %08x %08x  ->  %08x %08x   %s" % (enc[0], enc[1], a, v, tags))


if __name__ == "__main__":
    main()
