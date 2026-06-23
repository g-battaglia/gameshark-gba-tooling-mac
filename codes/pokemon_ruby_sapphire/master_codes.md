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
