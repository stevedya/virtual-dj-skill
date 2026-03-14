import os
from typing import List

import mido
from fastmcp import FastMCP

mcp = FastMCP("virtualdj")

DEFAULT_MIDI_PORT = os.getenv("VIRTUALDJ_MIDI_PORT", "IAC Driver Bus 1")


def get_output_names() -> List[str]:
    """Return available MIDI output port names."""
    return mido.get_output_names()


def open_port(port_name: str | None = None):
    """Open the configured MIDI output port."""
    selected_port = port_name or DEFAULT_MIDI_PORT
    return mido.open_output(selected_port)


def clamp_midi_value(value: int) -> int:
    """Clamp MIDI values into the valid range 0-127."""
    return max(0, min(127, int(value)))


def send_cc(control: int, value: int = 127, port_name: str | None = None) -> str:
    """
    Send a MIDI control change message to the configured output port.
    """
    safe_value = clamp_midi_value(value)
    selected_port = port_name or DEFAULT_MIDI_PORT

    try:
        with open_port(selected_port) as port:
            port.send(
                mido.Message(
                    "control_change",
                    control=int(control),
                    value=safe_value,
                )
            )
    except Exception as exc:
        raise RuntimeError(
            f"Failed to send MIDI CC{control}={safe_value} to '{selected_port}': {exc}"
        ) from exc

    return f"Sent CC{control}={safe_value} to '{selected_port}'"


@mcp.tool()
def healthcheck() -> str:
    """
    Check that the MCP server is running.
    """
    return "virtualdj_mcp is running"


@mcp.tool()
def list_midi_outputs() -> List[str]:
    """
    Return available MIDI output ports visible to Python.
    Useful for setup and debugging.
    """
    return get_output_names()


@mcp.tool()
def test_connection() -> str:
    """
    Validate that the configured MIDI port can be opened.
    """
    selected_port = DEFAULT_MIDI_PORT
    try:
        with open_port(selected_port):
            pass
    except Exception as exc:
        raise RuntimeError(
            f"Could not open MIDI port '{selected_port}': {exc}"
        ) from exc

    return f"Successfully opened MIDI port '{selected_port}'"


@mcp.tool()
def play() -> str:
    """
    Trigger play.
    VirtualDJ mapping example:
    CC1 -> deck 1 play
    """
    return send_cc(1)


@mcp.tool()
def pause() -> str:
    """
    Trigger pause.
    VirtualDJ mapping example:
    CC2 -> deck 1 pause
    """
    return send_cc(2)


@mcp.tool()
def crossfade(value: int) -> str:
    """
    Set the crossfader position from 0-127.
    VirtualDJ mapping example:
    CC3 -> crossfader
    """
    return send_cc(3, value)


@mcp.tool()
def echo() -> str:
    """
    Trigger an echo effect.
    VirtualDJ mapping example:
    CC4 -> effect_active 'echo'
    """
    return send_cc(4)


@mcp.tool()
def send_custom_cc(control: int, value: int = 127) -> str:
    """
    Send an arbitrary MIDI CC message.
    Useful for experimenting before dedicated tools are added.
    """
    return send_cc(control, value)


if __name__ == "__main__":
    mcp.run()