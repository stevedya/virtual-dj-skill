from dj.midi import send_cc, send_note


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