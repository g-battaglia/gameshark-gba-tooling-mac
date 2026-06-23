# Cheat codes catalog

Catalog of Action Replay V3 cheat codes for the GameShark / Action Replay GBA
device, organized so they can be re-flashed onto the device at any time with
`usbtool -C`.

## Format primer

The device stores codes **encrypted** with the AR V3 cipher (`../arcrypt.py`).
A single cheat (a "code" entry) is a list of 32-bit address/value pairs. The
whole database is a header (`num_games`, `num_cheats`) followed by, per game:

```
[4B num_cheats][20B game name]
  per cheat:
    [4B  flags:2 | num_words:30][20B cheat name]
    [num_words * 4B  encrypted pairs, little-endian]
```

`../convert_code_db.py` round-trips this between the binary `.ardb` blob and
JSON. `num_words` counts 32-bit words, i.e. `2 * num_pairs`.

## Master code (the `(m)` cheat) — how a game is recognized

The **first cheat** of a game is conventionally the master/enabler code. For an
AR V3 GBA game it is exactly **two pairs** that, when decrypted with
`seed(0)`, decode to:

| Pair # | Decrypted pattern   | Meaning                                    |
|--------|---------------------|--------------------------------------------|
| 1      | `c4XXXXXX 00008401` | Hook code: AR runs the cheat engine at ROM addr `XXXXXX` |
| 2      | `<gameid> 001dc0de` | Game-ID gate: `<gameid>` is the 4-byte GBA game code (little-endian) |

The device only activates a game's cheats if pair #2's `<gameid>` **matches the
game code in the ROM header** of the inserted cartridge. That is why codes are
region-specific: a USA master code (AXVE) will never fire on a EUR cart (AXVP).

### Region → game code (Ruby / Sapphire family)

| Title            | USA    | EUR    | JPN    |
|------------------|--------|--------|--------|
| Pokémon Ruby     | `AXVE` | `AXVP` | `AXVJ` |
| Pokémon Sapphire | `AXPE` | `AXPP` | `AXPJ` |

Decoded `<gameid>` values (the `a` of a decrypted `a 001dc0de` pair):

| Game code | `<gameid>` (hex) | encrypted pair (seed 0), for reference |
|-----------|------------------|----------------------------------------|
| AXVE      | `45565841`       | `530823d9 16558191` (USA Ruby)         |
| AXPE      | `45505841`       | `b4564efe 23f44bf2` (USA Sapphire)     |
| AXVP      | `50565841`       | `78fb7638 3f413aa3` (EUR Ruby)         |
| AXPP      | `50505841`       | `651bcd81 b9482575` (EUR Sapphire)     |

> The EUR Game-ID pairs above were generated locally and round-trip verified
> (encrypt→decrypt reproduces them). The hook line (`c4…… 00008401`) for the
> EUR ROMs must come from a verified EUR source — its address differs from the
> USA ROM.

## Verifying any code yourself

```sh
python3 codes/verify.py "DE00AAFD 2EBD05D0" "530823D9 16558191"
```

It decrypts each pair and flags hooks (`c4……`) and game-ID lines. Use it before
trusting any master code scraped from the web — sources routinely mislabel
regions. The decrypt result is ground truth.

## Files

- `device_dump_2026-06-23.json` — real codes read off the connected device
  (`usbtool -c`), fully decrypted. Authoritative example of a valid database.
- `pokemon_ruby_sapphire/` — Ruby & Sapphire codes, by region.
- `verify.py` — decrypt + classify any code pairs.
