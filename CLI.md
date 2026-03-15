# VirtualDJ CLI Usage

This file shows examples of how to run the VirtualDJ control CLI.

All commands assume you are inside the project directory and using `uv`.

---

## Health Check

Verify the skill is working.

```bash
uv run python virtualdj_skill.py healthcheck
```

Expected output

```json
{"ok": true, "result": "virtualdj skill is running"}
```

---

## List Available MIDI Outputs

Show all MIDI devices Python can send messages to.

```bash
uv run python virtualdj_skill.py list-outputs
```

Example output

```json
["IAC Driver Bus 1", "IAC Driver Bus 2"]
```

---

## Test MIDI Connection

Confirm the configured MIDI port can be opened.

```bash
uv run python virtualdj_skill.py test-connection
```

Expected output

```
Successfully opened MIDI port 'IAC Driver Bus 1'
```

---

## Toggle Deck Playback

Start or pause a deck.

Deck 1

```bash
uv run python virtualdj_skill.py play-pause --deck 1
```

Deck 2

```bash
uv run python virtualdj_skill.py play-pause --deck 2
```

VirtualDJ mappings required

```
0-BUTTON60 -> deck 1 play_pause
0-BUTTON61 -> deck 2 play_pause
```

---

## Move Crossfader

Set crossfader position (0–127).

All the way to Deck 1

```bash
uv run python virtualdj_skill.py crossfade 0
```

Center

```bash
uv run python virtualdj_skill.py crossfade 64
```

All the way to Deck 2

```bash
uv run python virtualdj_skill.py crossfade 127
```

VirtualDJ mapping

```
0-SLIDER1 -> crossfader
```

---

## Trigger Echo Effect

```bash
uv run python virtualdj_skill.py echo
```

VirtualDJ mapping

```
0-BUTTON62 -> effect_active 'echo'
```

---

## Send Custom MIDI Note

Useful for discovering new button mappings.

```bash
uv run python virtualdj_skill.py send-custom-note 60
```

VirtualDJ may show

```
0-BUTTON60
```

---

## Send Custom MIDI CC

Useful for discovering slider / encoder mappings.

```bash
uv run python virtualdj_skill.py send-custom-cc 1 --value 64
```

VirtualDJ may show

```
0-SLIDER1
```

---

## Example Mix

Start deck 2 and fade to it.

```bash
uv run python virtualdj_skill.py play-pause --deck 2
uv run python virtualdj_skill.py crossfade 127
```

Result

```
Deck 2 starts playing
Crossfader moves to Deck 2
```

---

## Default MIDI Port

The skill uses this MIDI port by default

```
IAC Driver Bus 1
```

Override with an environment variable

```bash
export VIRTUALDJ_MIDI_PORT="IAC Driver Bus 2"
```