import os
from typing import List

import mido

DEFAULT_MIDI_PORT = os.getenv("VIRTUALDJ_MIDI_PORT", "IAC Driver Bus 1")


def get_output_names() -> List[str]:
    """Return available MIDI output port names."""
    return mido.get_output_names()


def open_port(port_name: str | None = None):
    """
    Open the configured MIDI output port.

    Raises an error if the port cannot be opened.
    """
    selected_port = port_name or DEFAULT_MIDI_PORT
    return mido.open_output(selected_port)


def clamp_midi_value(value: int) -> int:
    """Clamp MIDI values into the valid MIDI range 0-127."""
    return max(0, min(127, int(value)))


def send_note(note: int, velocity: int = 127, port_name: str | None = None) -> str:
    """
    Send a MIDI NOTE ON message.

    VirtualDJ often interprets these as BUTTON inputs (e.g. BUTTON60).
    """
    safe_velocity = clamp_midi_value(velocity)
    selected_port = port_name or DEFAULT_MIDI_PORT

    try:
        with open_port(selected_port) as port:
            port.send(
                mido.Message(
                    "note_on",
                    note=int(note),
                    velocity=safe_velocity,
                )
            )
    except Exception as exc:
        raise RuntimeError(
            f"Failed to send NOTE {note} velocity={safe_velocity} "
            f"to '{selected_port}': {exc}"
        ) from exc

    return f"Sent NOTE {note} velocity={safe_velocity} to '{selected_port}'"


def send_cc(control: int, value: int = 127, port_name: str | None = None) -> str:
    """
    Send a MIDI Control Change message.

    VirtualDJ often interprets these as SLIDER or ENCODER inputs.
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
            f"Failed to send CC{control}={safe_value} to '{selected_port}': {exc}"
        ) from exc

    return f"Sent CC{control}={safe_value} to '{selected_port}'"


def test_connection(port_name: str | None = None) -> str:
    """
    Validate that the configured MIDI port can be opened.
    """
    selected_port = port_name or DEFAULT_MIDI_PORT

    try:
        with open_port(selected_port):
            pass
    except Exception as exc:
        raise RuntimeError(
            f"Could not open MIDI port '{selected_port}': {exc}"
        ) from exc

    return f"Successfully opened MIDI port '{selected_port}'"


def discover_ports() -> str:
    """
    Return a formatted list of available MIDI output ports.
    Useful for debugging configuration issues.
    """
    ports = get_output_names()

    if not ports:
        return "No MIDI output ports found."

    return "\n".join(f"{i + 1}. {name}" for i, name in enumerate(ports))


def send_note_test_range(start: int = 60, end: int = 68) -> str:
    """
    Send a quick range of NOTE messages for discovering VirtualDJ BUTTON mappings.
    """
    selected_port = DEFAULT_MIDI_PORT

    try:
        with open_port(selected_port) as port:
            for note in range(start, end + 1):
                port.send(mido.Message("note_on", note=note, velocity=127))
    except Exception as exc:
        raise RuntimeError(
            f"Failed during NOTE discovery on '{selected_port}': {exc}"
        ) from exc

    return f"Sent NOTE test range {start}-{end} to '{selected_port}'"


def send_cc_test_range(start: int = 1, end: int = 8, value: int = 64) -> str:
    """
    Send a range of CC messages for discovering SLIDER/ENCODER mappings.
    """
    selected_port = DEFAULT_MIDI_PORT

    safe_value = clamp_midi_value(value)

    try:
        with open_port(selected_port) as port:
            for control in range(start, end + 1):
                port.send(
                    mido.Message(
                        "control_change",
                        control=control,
                        value=safe_value,
                    )
                )
    except Exception as exc:
        raise RuntimeError(
            f"Failed during CC discovery on '{selected_port}': {exc}"
        ) from exc

    return (
        f"Sent CC test range {start}-{end} value={safe_value} "
        f"to '{selected_port}'"
    )
