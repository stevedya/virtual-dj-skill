# VirtualDJ Skill Controller

A lightweight Python skill that allows an AI agent (such as OpenClaw) to control **VirtualDJ** using MIDI commands.

The skill exposes simple commands such as:

- `play-pause --deck 1|2`
- `crossfade`
- `crossfade-auto`
- `echo`
- `send-custom-cc`
- `send-custom-note`
- `ping-note-range`
- `ping-cc-range`
- `search "query"`

These commands send **MIDI Control Change messages** to VirtualDJ through a **virtual MIDI port**, enabling AI-assisted DJ automation.

---

# Architecture

```
AI Agent (OpenClaw)
        ↓
Skill Runner (virtualdj_skill.py)
        ↓
Python MIDI (mido + rtmidi)
        ↓
Virtual MIDI Port
        ↓
VirtualDJ
```

The skill sends **MIDI Control Change messages** which VirtualDJ maps to actions.

---

# Requirements

- Python **3.10+**
- VirtualDJ installed
- A virtual MIDI device configured
- `uv` (Python package manager)

Dependencies used:

- `mido`
- `python-rtmidi`

---

# Setup

## 1. Clone the repository

```bash
git clone <your-repo-url>
cd virtualdj-mcp
```

---

## 2. Install Python (via uv)

If you do not already have Python ≥3.10:

```bash
uv python install 3.11
uv python pin 3.11
```

---

## 3. Install dependencies

```bash
uv add mido python-rtmidi
```

This creates:

```
.venv/
uv.lock
pyproject.toml
```

---

# Configure Virtual MIDI

## macOS (IAC Driver)

1. Open **Audio MIDI Setup**
2. Select **Window → Show MIDI Studio**
3. Double-click **IAC Driver**
4. Enable **Device is online**
5. Create a port

Example:

```
IAC Driver Bus 1
```

---

## Windows

Install:

```
loopMIDI
```

Create a virtual port such as:

```
VirtualDJ_AI
```

---

# Configure VirtualDJ

Open:

```
VirtualDJ → Settings → Controllers
```

Add the virtual MIDI device and create mappings such as:

```
CC1 → deck 1 play
CC2 → deck 1 pause
CC3 → crossfader
CC4 → effect_active 'echo'
```

These correspond to the control change messages sent by the skill.

---

# Running the Skill

Run commands using uv:

```bash
uv run python virtualdj_skill.py <command>
```

Examples:

```
uv run python virtualdj_skill.py play-pause --deck 1
uv run python virtualdj_skill.py crossfade 64
uv run python virtualdj_skill.py crossfade-auto
uv run python virtualdj_skill.py echo
uv run python virtualdj_skill.py ping-note-range --start 60 --end 68
uv run python virtualdj_skill.py ping-cc-range --start 1 --end 8 --value 64
uv run python virtualdj_skill.py search "daft punk one more time"
```

---

# Environment Configuration

Set the MIDI port used by the skill:

```bash
export VIRTUALDJ_MIDI_PORT="IAC Driver Bus 1"
```

If this variable is not set, the default port used is:

```
IAC Driver Bus 1
```

---

# Testing MIDI Connectivity

You can list available MIDI outputs with:

```bash
uv run python virtualdj_skill.py list-outputs
```

Or test the configured port:

```bash
uv run python virtualdj_skill.py test-connection
```

You can also test manually:

```python
import mido

print(mido.get_output_names())
```

Example output:

```
['IAC Driver Bus 1']
```

Ensure the name matches the configured MIDI port.

---

# Example AI Commands

An AI assistant could issue commands like:

```
Play the track
Pause the track
Move the crossfader to the center
Trigger echo effect
```

These will call the skill and send MIDI commands to VirtualDJ.

---

# Repository Structure

```
virtualdj-mcp/
│
├── SKILL.md
├── README.md
├── virtualdj_skill.py
├── test_midi.py
│
└── dj/
    ├── __init__.py
    ├── midi.py
    └── commands.py
```

---

# Future Improvements

Possible extensions:

- Track loading from local library
- BPM detection and beat matching
- Automatic transitions
- Playlist selection
- AI-assisted mixing strategies
- Track energy analysis
- Deck state awareness
- MIDI controller learning
- Integration with hardware DJ controllers

---

# License

MIT
