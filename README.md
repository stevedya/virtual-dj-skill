# VirtualDJ MCP Controller

A small **MCP (Model Context Protocol) server** that allows an AI agent to control **VirtualDJ** using MIDI commands.

The server exposes simple tools like:

* `play`
* `pause`
* `crossfade`
* `echo`

These tools send MIDI control messages to VirtualDJ through a **virtual MIDI port**, allowing AI assistants to automate mixing actions.

---

# How It Works

```
AI Agent (OpenClaw / MCP Client)
        ↓
MCP Server (this repo)
        ↓
Python MIDI (mido)
        ↓
Virtual MIDI Port
        ↓
VirtualDJ
```

The MCP server sends MIDI control change messages which VirtualDJ maps to actions.

---

# Requirements

* Python 3.9+
* VirtualDJ installed
* Virtual MIDI device configured
* `mido`
* `python-rtmidi`
* `fastmcp`

---

# Setup

## 1. Clone the repository

```
git clone <your-repo-url>
cd virtualdj-mcp
```

---

## 2. Create a Python virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```
pip install mido python-rtmidi fastmcp
```

(Optional)

```
pip freeze > requirements.txt
```

---

# Configure Virtual MIDI

## macOS (IAC Driver)

1. Open **Audio MIDI Setup**
2. Select **Window → Show MIDI Studio**
3. Double-click **IAC Driver**
4. Enable **Device is online**
5. Create a port (default: `IAC Driver Bus 1`)

---

## Windows

Install:

```
loopMIDI
```

Create a virtual port like:

```
VirtualDJ_AI
```

---

# Configure VirtualDJ

Open **VirtualDJ → Settings → Controllers**

Add the virtual MIDI device and create mappings such as:

```
CC1 → deck 1 play
CC2 → deck 1 pause
CC3 → crossfader
CC4 → effect_active 'echo'
```

These correspond to the control change messages sent by the MCP server.

---

# Running the MCP Server

Activate your environment:

```
source .venv/bin/activate
```

Run the server:

```
python virtualdj_mcp.py
```

The MCP server will start and expose its tools to any MCP-compatible client.

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
          "command": "/path/to/virtualdj-mcp/.venv/bin/python",
          "args": ["/path/to/virtualdj-mcp/virtualdj_mcp.py"],
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

# Testing

You can test MIDI connectivity with:

```python
import mido
print(mido.get_output_names())
```

Example output:

```
['IAC Driver Bus 1']
```

Ensure the name matches the port configured in the server.

---

# Example AI Commands

Once connected, an AI agent could issue commands like:

```
Play the track
Trigger echo
Move the crossfader to the middle
Pause deck one
```

These will trigger the corresponding MCP tools and send MIDI to VirtualDJ.

---

# Future Improvements

Possible extensions:

* Track loading from local library
* BPM detection and beat matching
* Automatic transitions
* Playlist selection
* AI-assisted mixing strategies
* Track energy analysis

---

# License

MIT
