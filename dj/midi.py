import os
from typing import List

import mido

DEFAULT_MIDI_PORT = os.getenv("VIRTUALDJ_MIDI_PORT", "IAC Driver Bus 1")


def get_output_names() -> List[str]:
    """Return available MIDI output port names."""
    return mido.get_output_names()


def open_port(port_name: str | None = None):
    """Open the configured MIDI output port."""
    selected_port = port_name or DEFAULT_MIDI_PORT
    return mido.open_output(selected_port)


def clamp_midi_value(value: int) -> int:
    """Clamp MIDI values into the valid MIDI range 0-127."""
    return max(0, min(127, int(value)))


def send_cc(control: int, value: int = 127, port_name: str | None = None) -> str:
    """Send a MIDI control change message to the configured output port."""
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


def test_connection(port_name: str | None = None) -> str:
    """Validate that the configured MIDI port can be opened."""
    selected_port = port_name or DEFAULT_MIDI_PORT

    try:
        with open_port(selected_port):
            pass
    except Exception as exc:
        raise RuntimeError(
            f"Could not open MIDI port '{selected_port}': {exc}"
        ) from exc

    return f"Successfully opened MIDI port '{selected_port}'"