from dj.midi import send_cc


def play() -> str:
    """
    Trigger play.
    VirtualDJ mapping example:
    CC1 -> deck 1 play
    """
    return send_cc(1)


def pause() -> str:
    """
    Trigger pause.
    VirtualDJ mapping example:
    CC2 -> deck 1 pause
    """
    return send_cc(2)


def crossfade(value: int) -> str:
    """
    Set the crossfader position from 0-127.
    VirtualDJ mapping example:
    CC3 -> crossfader
    """
    return send_cc(3, value)


def echo() -> str:
    """
    Trigger an echo effect.
    VirtualDJ mapping example:
    CC4 -> effect_active 'echo'
    """
    return send_cc(4)


def send_custom_cc(control: int, value: int = 127) -> str:
    """
    Send an arbitrary MIDI CC message.
    Useful for experimenting before dedicated commands are added.
    """
    return send_cc(control, value)