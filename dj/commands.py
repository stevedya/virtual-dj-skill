from dj.keyboard import virtualdj_search, virtualdj_select_result
from dj.library import list_library_results
from dj.midi import send_cc, send_cc_test_range, send_note, send_note_test_range


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


def select_result(
    result_index: int,
    app_name: str = "VirtualDJ",
    no_reset: bool = False,
) -> str:
    """
    Move browser selection to a 1-based result index.
    """
    return virtualdj_select_result(
        result_index=result_index,
        app_name=app_name,
        reset_to_top=not no_reset,
    )


def list_results(
    query: str,
    limit: int = 10,
    database_xml: str | None = None,
) -> list[dict[str, str]]:
    """
    List matching tracks from VirtualDJ database.xml.
    """
    return list_library_results(query=query, limit=limit, database_xml=database_xml)


def load_deck(deck: int) -> str:
    """
    Load selected browser track to a deck.

    VirtualDJ mapping example:
    BUTTON71 -> deck 1 load
    BUTTON72 -> deck 2 load
    """
    note_map = {
        1: 71,
        2: 72,
    }
    if deck not in note_map:
        raise ValueError(f"Unsupported deck: {deck}")
    return send_note(note_map[deck])


def search_select(
    query: str,
    result_index: int = 1,
    app_name: str = "VirtualDJ",
) -> str:
    """
    Search in VirtualDJ, then select a result index.
    """
    search_msg = search_library(query=query, app_name=app_name)
    select_msg = select_result(result_index=result_index, app_name=app_name)
    return f"{search_msg}; {select_msg}"


def search_load(
    query: str,
    deck: int,
    result_index: int = 1,
    app_name: str = "VirtualDJ",
) -> str:
    """
    Search, select result, and load to deck.
    """
    select_msg = search_select(query=query, result_index=result_index, app_name=app_name)
    load_msg = load_deck(deck)
    return f"{select_msg}; {load_msg}"


def add_to_sidelist() -> str:
    """
    Add selected browser track to sidelist.

    VirtualDJ mapping example:
    BUTTON73 -> sidelist_add
    """
    return send_note(73)


def start_automix() -> str:
    """
    Start/toggle automix.

    VirtualDJ mapping example:
    BUTTON75 -> automix
    """
    return send_note(75)


def add_to_automix_next() -> str:
    """
    Add selected browser track to automix next queue.

    VirtualDJ mapping example:
    BUTTON74 -> automix_add_next
    """
    return send_note(74)
