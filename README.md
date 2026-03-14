# VirtualDJ MCP Controller

A lightweight **MCP (Model Context Protocol) server** that allows an AI agent to control **VirtualDJ** using MIDI commands.

The server exposes simple tools such as:

- `play`
- `pause`
- `crossfade`
- `echo`

These tools send MIDI control messages to VirtualDJ through a **virtual MIDI port**, allowing AI assistants to automate mixing actions.

---

# Architecture

```
AI Agent (OpenClaw / MCP Client)
        ↓
MCP Server (this repo)
        ↓
Python MIDI (mido + rtmidi)
        ↓
Virtual MIDI Port
        ↓
VirtualDJ
```

The MCP server sends **MIDI Control Change messages** which VirtualDJ maps to actions.

---

# Requirements

- Python **3.10+**
- VirtualDJ installed
- A virtual MIDI device configured
- `uv` (Python package manager)

Dependencies used:

- `fastmcp`
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

If you don't already have Python ≥3.10:

```bash
uv python install 3.11
uv python pin 3.11
```

---

## 3. Install dependencies

```bash
uv add mido python-rtmidi fastmcp
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
5. Create a port (example: `IAC Driver Bus 1`)

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

These correspond to the **control change messages** sent by the MCP server.

---

# Running the MCP Server

Run the server with uv:

```bash
uv run python virtualdj_mcp.py
```

The MCP server will start and expose its tools to MCP-compatible clients.

---

# Using With OpenClaw

Add the MCP server to your OpenClaw configuration.

Example:

```json
{
  "plugins": {
    "mcp": {
      "servers": {
        "virtualdj": {
          "command": "uv",
          "args": ["run", "python", "virtualdj_mcp.py"],
          "cwd": "/path/to/virtualdj-mcp",
          "env": {
            "VIRTUALDJ_MIDI_PORT": "IAC Driver Bus 1"
          }
        }
      }
    }
  }
}
```

Restart OpenClaw after updating the configuration.

---

# Testing MIDI Connectivity

You can test MIDI devices with:

```bash
uv run python
```

Then run:

```python
import mido

print("Inputs:", mido.get_input_names())
print("Outputs:", mido.get_output_names())
```

Example output:

```
Outputs:
['IAC Driver Bus 1']
```

Ensure the name matches the port configured in your server.

---

# Example AI Commands

Once connected, an AI agent could issue commands like:

```
Play the track
Trigger echo
Move the crossfader to the middle
Pause deck one
```

These trigger MCP tools that send MIDI commands to VirtualDJ.

---

# Future Improvements

Potential extensions:

- Track loading from local library
- BPM detection and beat matching
- Automatic transitions
- Playlist selection
- AI-assisted mixing strategies
- Track energy analysis
- Deck state awareness
- MIDI controller learning

---

# License

MIT