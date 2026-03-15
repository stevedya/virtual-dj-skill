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
- crossfade auto
- echo
- sending custom MIDI CC messages
- sending custom MIDI note messages
- pinging key ranges for mapping discovery
- searching library text (macOS keyboard automation)
- listing search matches from VirtualDJ database
- selecting specific search result rows
- loading selected result to deck 1 or 2
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

### Crossfade auto

```bash
uv run python virtualdj_skill.py crossfade-auto
```

Triggers a dedicated button for VirtualDJ's automatic crossfade action.

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

### Search library text

```bash
uv run python virtualdj_skill.py search "daft punk one more time"
```

Sends keyboard input to VirtualDJ search using macOS automation.

Options:

```bash
uv run python virtualdj_skill.py search "disco" --no-submit
uv run python virtualdj_skill.py search "house" --no-shortcut
uv run python virtualdj_skill.py search "drum and bass" --app "VirtualDJ"
```

---

### List results

```bash
uv run python virtualdj_skill.py list-results "daft punk" --limit 10
```

Reads VirtualDJ `database.xml` and returns matching tracks.

---

### Select result row

```bash
uv run python virtualdj_skill.py select-result 3
```

Selects the 3rd result (1-based index) in the current browser list.

---

### Load selected result to deck

```bash
uv run python virtualdj_skill.py load-deck --deck 1
uv run python virtualdj_skill.py load-deck --deck 2
```

Requires VirtualDJ mapping:

```
0-BUTTON71 -> deck 1 load
0-BUTTON72 -> deck 2 load
```

---

### Search and load in one command

```bash
uv run python virtualdj_skill.py search-load "daft punk" --deck 1 --result 2
```

---

## Multi-Step Mix Recipes

Use these for predictable transition workflows.

### Recipe: Search track, load to deck 2, play, auto-crossfade

```bash
uv run python virtualdj_skill.py search-load "nickelback someday" --deck 2 --result 1
uv run python virtualdj_skill.py play-pause --deck 2
uv run python virtualdj_skill.py crossfade-auto
```

One-line version:

```bash
uv run python virtualdj_skill.py search-load "nickelback someday" --deck 2 --result 1 && \
uv run python virtualdj_skill.py play-pause --deck 2 && \
uv run python virtualdj_skill.py crossfade-auto
```

### Recipe: Explicit step-by-step (without search-load helper)

```bash
uv run python virtualdj_skill.py search "nickelback someday"
uv run python virtualdj_skill.py select-result 1
uv run python virtualdj_skill.py load-deck --deck 2
uv run python virtualdj_skill.py play-pause --deck 2
uv run python virtualdj_skill.py crossfade-auto
```

Tip: `play-pause` is a toggle. If deck 2 is already playing, this command will pause it.

---

## Example VirtualDJ MIDI Mappings

Inside VirtualDJ → Settings → Controllers, you can map incoming MIDI controls.

Example mappings:

```
0-BUTTON60 -> deck 1 play_pause
0-BUTTON61 -> deck 2 play_pause
0-SLIDER1 -> crossfader
0-BUTTON63 -> crossfader_auto
0-BUTTON62 -> effect_active 'echo'
0-BUTTON71 -> deck 1 load
0-BUTTON72 -> deck 2 load
```

These correspond to the commands implemented in the skill.

---

## Notes

- MIDI values are clamped to the valid range of **0–127**.
- The skill sends **MIDI note** and **MIDI Control Change** messages.
- `search` requires macOS Accessibility permissions for the terminal app.
- `list-results` reads `~/Documents/VirtualDJ/database.xml` by default.
- Additional commands can be added easily in `dj/commands.py`.

# Mapping Notes

## 2026-03-14
- note_on 60 appears in VirtualDJ as 0-BUTTON60
- note_on 61 appears in VirtualDJ as 0-BUTTON61
- cc 1 appears as 0-SLIDER1
- cc 2 appears as 0-SLIDER2
- VirtualDJ normalizes raw MIDI into internal control names for this generic device
