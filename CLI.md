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

## Quick Crossfader Presets

Useful while testing transitions.

Left

```bash
uv run python virtualdj_skill.py crossfade-left
```

Center

```bash
uv run python virtualdj_skill.py crossfade-center
```

Right

```bash
uv run python virtualdj_skill.py crossfade-right
```

---

## Auto Crossfade

Trigger VirtualDJ's automatic crossfade action.

```bash
uv run python virtualdj_skill.py crossfade-auto
```

VirtualDJ mapping

```
0-BUTTON63 -> crossfader_auto
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

## Ping Note Range (Button Discovery)

Fire a range of note events so VirtualDJ shows multiple `0-BUTTONXX` controls.

```bash
uv run python virtualdj_skill.py ping-note-range --start 60 --end 68
```

---

## Ping CC Range (Slider Discovery)

Fire a range of CC events so VirtualDJ shows multiple slider controls.

```bash
uv run python virtualdj_skill.py ping-cc-range --start 1 --end 8 --value 64
```

---

## Search Library (Keyboard Automation)

Type text into VirtualDJ search.

```bash
uv run python virtualdj_skill.py search "daft punk one more time"
```

Options:

```bash
uv run python virtualdj_skill.py search "disco" --no-submit
uv run python virtualdj_skill.py search "house" --no-shortcut
uv run python virtualdj_skill.py search "drum and bass" --app "VirtualDJ"
```

Notes:

- This command uses macOS `osascript` keyboard events.
- Grant Accessibility permissions to your terminal app.
- VirtualDJ should be running.

---

## List Results (From database.xml)

Searches VirtualDJ's local database index and returns matching tracks.

```bash
uv run python virtualdj_skill.py list-results "daft punk" --limit 10
```

Optional database path:

```bash
uv run python virtualdj_skill.py list-results "house" --database ~/Documents/VirtualDJ/database.xml
```

---

## Select Search Result Row

Select result row by 1-based index in the active browser list.

```bash
uv run python virtualdj_skill.py select-result 3
```

---

## Load Selected Track to Deck

```bash
uv run python virtualdj_skill.py load-deck --deck 1
uv run python virtualdj_skill.py load-deck --deck 2
```

VirtualDJ mappings required:

```
0-BUTTON71 -> deck 1 load
0-BUTTON72 -> deck 2 load
```

---

## Browser Queue Actions

Add selected track to sidelist:

```bash
uv run python virtualdj_skill.py add-to-sidelist
```

Add selected track to automix:

```bash
uv run python virtualdj_skill.py add-to-automix
```

Start/toggle automix:

```bash
uv run python virtualdj_skill.py automix-start
```

Add selected track to play next:

```bash
uv run python virtualdj_skill.py add-to-play-next
```

VirtualDJ mappings required:

```
0-BUTTON73 -> sidelist_add
0-BUTTON74 -> automix_add
0-BUTTON75 -> automix
0-BUTTON76 -> play_next
```

---

## Search + Select

```bash
uv run python virtualdj_skill.py search-select "daft punk" --result 2
```

---

## Search + Load

```bash
uv run python virtualdj_skill.py search-load "daft punk" --deck 1 --result 2
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
