from fastmcp import FastMCP
import mido
import os

mcp = FastMCP("virtualdj")

MIDI_PORT = os.getenv("VIRTUALDJ_MIDI_PORT", "IAC Driver Bus 1")
port = mido.open_output(MIDI_PORT)

def send_cc(cc: int, value: int = 127) -> None:
    port.send(mido.Message("control_change", control=cc, value=value))

@mcp.tool()
def play() -> str:
    send_cc(1)
    return "Play triggered"

@mcp.tool()
def pause() -> str:
    send_cc(2)
    return "Pause triggered"

@mcp.tool()
def crossfade(value: int) -> str:
    value = max(0, min(127, value))
    send_cc(3, value)
    return f"Crossfader set to {value}"

@mcp.tool()
def echo() -> str:
    send_cc(4)
    return "Echo triggered"

if __name__ == "__main__":
    mcp.run()
