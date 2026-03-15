from dj.midi import send_cc, send_cc_test_range, send_note, send_note_test_range
from dj.keyboard import virtualdj_search


def deck_play_pause(deck: int) -> str:
    """
    Toggle play/pause for a deck.

    VirtualDJ mapping:
    BUTTON60 -> deck 1 play_pause
    BUTTON61 -> deck 2 play_pause
    """
    note_map = {
        1: 60,
        2: 61,
    }

    if deck not in note_map:
        raise ValueError(f"Unsupported deck: {deck}")

    return send_note(note_map[deck])


def crossfade(value: int) -> str:
    """
    Set the crossfader position from 0-127.

    VirtualDJ mapping example:
    SLIDER1 -> crossfader
    """
    return send_cc(1, value)


def crossfade_left() -> str:
    """Move crossfader fully left (deck 1 side)."""
    return crossfade(0)


def crossfade_center() -> str:
    """Move crossfader to center."""
    return crossfade(64)


def crossfade_right() -> str:
    """Move crossfader fully right (deck 2 side)."""
    return crossfade(127)


def crossfade_auto() -> str:
    """
    Trigger VirtualDJ automatic crossfade.

    VirtualDJ mapping example:
    BUTTON63 -> crossfader_auto
    """
    return send_note(63)


def echo() -> str:
    """
    Trigger an echo-related button action.

    Update the mapped note if you assign echo to a different VirtualDJ button.
    """
    return send_note(62)


def send_custom_note(note: int, velocity: int = 127) -> str:
    """
    Send an arbitrary MIDI note.
    """
    return send_note(note, velocity)


def send_custom_cc(control: int, value: int = 127) -> str:
    """
    Send an arbitrary MIDI CC message.
    """
    return send_cc(control, value)


def ping_note_range(start: int = 60, end: int = 68) -> str:
    """
    Send a note range to discover VirtualDJ BUTTON mappings.
    """
    return send_note_test_range(start, end)


def ping_cc_range(start: int = 1, end: int = 8, value: int = 64) -> str:
    """
    Send a CC range to discover VirtualDJ SLIDER/ENCODER mappings.
    """
    return send_cc_test_range(start, end, value)


def search_library(
    query: str,
    app_name: str = "VirtualDJ",
    no_shortcut: bool = False,
    no_submit: bool = False,
) -> str:
    """
    Send a typed search query to the VirtualDJ browser.
    """
    return virtualdj_search(
        query=query,
        app_name=app_name,
        open_search_shortcut=not no_shortcut,
        submit=not no_submit,
    )
