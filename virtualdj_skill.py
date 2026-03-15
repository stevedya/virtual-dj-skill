import argparse
import json

from dj.commands import (
    crossfade,
    crossfade_auto,
    crossfade_center,
    crossfade_left,
    crossfade_right,
    deck_play_pause,
    echo,
    ping_cc_range,
    ping_note_range,
    send_custom_cc,
    send_custom_note,
)
from dj.midi import get_output_names, test_connection


def main() -> None:
    parser = argparse.ArgumentParser(description="VirtualDJ skill runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("healthcheck")
    subparsers.add_parser("list-outputs")
    subparsers.add_parser("test-connection")
    subparsers.add_parser("echo")

    play_pause_parser = subparsers.add_parser("play-pause")
    play_pause_parser.add_argument("--deck", type=int, required=True, choices=[1, 2])

    crossfade_parser = subparsers.add_parser("crossfade")
    crossfade_parser.add_argument("value", type=int)
    subparsers.add_parser("crossfade-left")
    subparsers.add_parser("crossfade-center")
    subparsers.add_parser("crossfade-right")
    subparsers.add_parser("crossfade-auto")

    custom_cc_parser = subparsers.add_parser("send-custom-cc")
    custom_cc_parser.add_argument("control", type=int)
    custom_cc_parser.add_argument("--value", type=int, default=127)

    custom_note_parser = subparsers.add_parser("send-custom-note")
    custom_note_parser.add_argument("note", type=int)
    custom_note_parser.add_argument("--velocity", type=int, default=127)

    ping_notes_parser = subparsers.add_parser("ping-note-range")
    ping_notes_parser.add_argument("--start", type=int, default=60)
    ping_notes_parser.add_argument("--end", type=int, default=68)

    ping_cc_parser = subparsers.add_parser("ping-cc-range")
    ping_cc_parser.add_argument("--start", type=int, default=1)
    ping_cc_parser.add_argument("--end", type=int, default=8)
    ping_cc_parser.add_argument("--value", type=int, default=64)

    args = parser.parse_args()

    if args.command == "healthcheck":
        result = "virtualdj skill is running"
    elif args.command == "list-outputs":
        result = get_output_names()
    elif args.command == "test-connection":
        result = test_connection()
    elif args.command == "play-pause":
        result = deck_play_pause(args.deck)
    elif args.command == "crossfade":
        result = crossfade(args.value)
    elif args.command == "crossfade-left":
        result = crossfade_left()
    elif args.command == "crossfade-center":
        result = crossfade_center()
    elif args.command == "crossfade-right":
        result = crossfade_right()
    elif args.command == "crossfade-auto":
        result = crossfade_auto()
    elif args.command == "echo":
        result = echo()
    elif args.command == "send-custom-cc":
        result = send_custom_cc(args.control, args.value)
    elif args.command == "send-custom-note":
        result = send_custom_note(args.note, args.velocity)
    elif args.command == "ping-note-range":
        result = ping_note_range(args.start, args.end)
    elif args.command == "ping-cc-range":
        result = ping_cc_range(args.start, args.end, args.value)
    else:
        raise RuntimeError(f"Unknown command: {args.command}")

    print(json.dumps({"ok": True, "result": result}))


if __name__ == "__main__":
    main()
