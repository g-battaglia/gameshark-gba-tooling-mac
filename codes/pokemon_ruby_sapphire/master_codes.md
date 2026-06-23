# Pokémon Ruby & Sapphire — Action Replay V3 codes

Game codes: **AXVP** (Ruby EUR), **AXPP** (Sapphire EUR), `AXVE`/`AXPE` (USA),
`AXVJ`/`AXPJ` (JPN).

## Master codes — VERIFIED

The `(m)` / "Must Be On" cheat. The device activates a game only when the
decrypted game-ID line matches the cartridge's game code. All pairs below were
verified with `../verify.py`.

### EUR (AXVP / AXPP) — use these for European cartridges

Both titles share the same EUR hook line; only the game-ID line differs.

```
# Ruby EUR (AXVP)
F57C7BCB ADC632B9      -> C40010AE 00008401   (hook, rom 0x10ae)
78FB7638 3F413AA3      -> 50565841 001DC0DE   (AXVP)

# Sapphire EUR (AXPP)
F57C7BCB ADC632B9      -> C40010AE 00008401   (hook)
651BCD81 B9482575      -> 50505841 001DC0DE   (AXPP)
```

- The EUR game-ID lines were **generated locally** (encrypt of AXVP/AXPP with
  `001dc0de` under `seed(0)`) and round-trip verified.
- The EUR hook `F57C7BCB ADC632B9` came from the GameHacking.org page for
  *Pokémon Ruby (Europe) AGB-AXVP* (game 5639). Note that page also lists a
  corrupted game-ID line that decodes to "AXVF" (nonexistent) — ignore it; the
  correct game-ID line is the AXVP one above.

### Variant cartridge: AXVI (the Ruby cart in this project's device)

The actual Ruby cartridge read by the connected device reports game code
**`AXVI`**, not the standard EUR `AXVP` (likely a reproduction/variant cart).
The EUR hook is identical (the ROM body is the same); only the game-ID line
differs. Generated locally and round-trip verified:

```
# Ruby variant (AXVI) — matches this cart
F57C7BCB ADC632B9      -> C40010AE 00008401   (hook)
93A1C658 8DD5F1D0      -> 49565841 001DC0DE   (AXVI)
```

To build the master for any 4-byte game code, encrypt `(u32(code), 0x001dc0de)`
under `arcrypt.seed(0)`:
```python
import arcrypt, struct
code = "AXVI"  # or AXVP, AXPP, etc.
ea, eb = arcrypt.encrypt(arcrypt.seed(0), (struct.unpack("<I", code.encode())[0], 0x001dc0de))
```

## Wild Pokémon Modifier (all 386) — two sets, two masters

The 386 wild modifiers come from two different FAQ sets that use **different
hook lines**, so they live in different games on the device:

| Range | FAQ set | Hook line | Decrypted pattern | Lives in game |
|-------|---------|-----------|-------------------|---------------|
| #001–251 (Kanto/Johto) | 1.2.1 (old) | `F57C7BCB ADC632B9` (rom 0x10ae, the std EUR master) | enabler `39E924C4 4136A9DD` + species → decodes to `0x00002000+dex` | `POKEMON RUBY` / `SAPPHIRE` (alongside the generic cheats) |
| #252–386 (Hoenn) | 1.2.4 (new) | `A2E564FE 0FB58A54` (rom 0x3a82a) | species alone → decodes to `write 0x02307d22 = 0x115+(dex-252)` (internal species index) | `RUBY HOENN` / `SAPPHIRE HOENN` (dedicated games) |

Both Hoenn games reuse the same game-ID line as the main games (AXVI/AXPP), so
the same cartridge matches all four entries. All 386 species codes are bulk-
verified to decode to their exact expected value (`verify.py`); #343 Swalot
was reconstructed cryptographically from the pattern after a transcription error.

- `wild_modifier_001_251.tsv` — Kanto/Johto species codes (1.2.1, use with enabler + std master)
- `wild_modifier_252_386.tsv` — Hoenn species codes (1.2.4, use with new master `A2E564FE 0FB58A54`)
- `database_full.ardb` — the flashed 9-game, 1026-cheat blob


### USA (AXVE / AXPE) — for reference only

```
# Ruby USA (AXVE)
DE00AAFD 2EBD05D0      -> C4000430 00008401   (hook, rom 0x430)
530823D9 16558191      -> 45565841 001DC0DE   (AXVE)

# Sapphire USA (AXPE)
DE00AAFD 2EBD05D0      -> C4000430 00008401
B4564EFE 23F44BF2      -> 45505841 001DC0DE   (AXPE)
```

## Cheat codes (region-independent body)

Per mastersord's GameFAQs FAQ: the Ruby/Sapphire EUR and USA ROMs are
**memory-identical** — only the master code differs. So the cheat bodies
extracted from the USA AR V3 FAQ (loadingNOW) work on the EUR cartridge when
paired with the EUR master above. Every cheat below should be re-verified with
`../verify.py` before flashing: decrypt it and check the operation is sane
(`04xxxxxx`/`02xxxxxx` = write 32/16-bit, etc.).

See `cheats_eur.json` for the assembled, verified cheat set ready to merge into
the device database.
