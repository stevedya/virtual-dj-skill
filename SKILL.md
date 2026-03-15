---
name: virtual-dj-skill
description: This skill allows OpenClaw to control VirtualDJ by sending MIDI Control Change messages through a virtual MIDI port.
metadata: {"clawdbot":{"emoji":"💿","requires":{"bins":["python"],"env":["VIRTUALDJ_MIDI_PORT"]},"primaryEnv":"VIRTUALDJ_MIDI_PORT"}}
---

# VirtualDJ Skill

## Purpose

It can be used for simple DJ automation tasks such as:

- play/pause toggle
- crossfade
- echo
- sending custom MIDI CC messages
- sending custom MIDI note messages
- pinging key ranges for mapping discovery
- listing available MIDI outputs
- testing MIDI connectivity

The skill runs locally and communicates with VirtualDJ through a virtual MIDI device.

---

## Requirements

- Python 3.10+
- `uv` package manager
- VirtualDJ installed
- A configured virtual MIDI port

Dependencies:

- mido
- python-rtmidi

Install dependencies:

```bash
uv add mido python-rtmidi
```

---

## Environment

Set the MIDI port name using an environment variable:

```bash
export VIRTUALDJ_MIDI_PORT="IAC Driver Bus 1"
```

If not set, the default port used is:

```
IAC Driver Bus 1
```

---

## Files

```
virtualdj_skill.py   CLI entrypoint for the skill
dj/midi.py           low-level MIDI helpers
dj/commands.py       DJ command functions
```

---

## Supported Commands

### Healthcheck

```bash
uv run python virtualdj_skill.py healthcheck
```

Returns a confirmation that the skill is running.

---

### List MIDI outputs

```bash
uv run python virtualdj_skill.py list-outputs
```

Shows available MIDI output devices detected by Python.

---

### Test MIDI connection

```bash
uv run python virtualdj_skill.py test-connection
```

Attempts to open the configured MIDI port to verify connectivity.

---

### Play/Pause toggle

```bash
uv run python virtualdj_skill.py play-pause --deck 1
```

Toggles playback for the selected deck.

---

### Crossfade

```bash
uv run python virtualdj_skill.py crossfade 64
```

Sets the crossfader position from 0 to 127.

Examples:

```
0   = full left
64  = center
127 = full right
```

---

### Echo effect

```bash
uv run python virtualdj_skill.py echo
```

Triggers an echo effect mapped in VirtualDJ.

---

### Send custom MIDI control change

```bash
uv run python virtualdj_skill.py send-custom-cc 12 --value 127
```

Sends an arbitrary MIDI control change message.

Useful for testing mappings before creating dedicated commands.

---

### Send custom MIDI note

```bash
uv run python virtualdj_skill.py send-custom-note 60 --velocity 127
```

Sends an arbitrary MIDI note message for button mapping tests.

---

### Ping note range (mapping discovery)

```bash
uv run python virtualdj_skill.py ping-note-range --start 60 --end 68
```

Sends a range of notes so VirtualDJ exposes multiple `BUTTON` keys quickly.

---

### Ping CC range (mapping discovery)

```bash
uv run python virtualdj_skill.py ping-cc-range --start 1 --end 8 --value 64
```

Sends a range of CC controls so VirtualDJ exposes multiple slider/encoder keys.

---

## Example VirtualDJ MIDI Mappings

Inside VirtualDJ → Settings → Controllers, you can map incoming MIDI controls.

Example mappings:

```
0-BUTTON60 -> deck 1 play_pause
0-BUTTON61 -> deck 2 play_pause
0-SLIDER1 -> crossfader
0-BUTTON62 -> effect_active 'echo'
```

These correspond to the commands implemented in the skill.

---

## Notes

- MIDI values are clamped to the valid range of **0–127**.
- The skill currently sends **MIDI Control Change messages only**.
- Additional commands can be added easily in `dj/commands.py`.

# Mapping Notes

## 2026-03-14
- note_on 60 appears in VirtualDJ as 0-BUTTON60
- note_on 61 appears in VirtualDJ as 0-BUTTON61
- cc 1 appears as 0-SLIDER1
- cc 2 appears as 0-SLIDER2
- VirtualDJ normalizes raw MIDI into internal control names for this generic device
