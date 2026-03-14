import argparse
import json

from dj.commands import crossfade, echo, pause, play, send_custom_cc
from dj.midi import get_output_names, test_connection


def main() -> None:
    parser = argparse.ArgumentParser(description="VirtualDJ skill runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("healthcheck")
    subparsers.add_parser("list-outputs")
    subparsers.add_parser("test-connection")
    subparsers.add_parser("play")
    subparsers.add_parser("pause")
    subparsers.add_parser("echo")

    crossfade_parser = subparsers.add_parser("crossfade")
    crossfade_parser.add_argument("value", type=int)

    custom_cc_parser = subparsers.add_parser("send-custom-cc")
    custom_cc_parser.add_argument("control", type=int)
    custom_cc_parser.add_argument("--value", type=int, default=127)

    args = parser.parse_args()

    if args.command == "healthcheck":
        result = "virtualdj skill is running"
    elif args.command == "list-outputs":
        result = get_output_names()
    elif args.command == "test-connection":
        result = test_connection()
    elif args.command == "play":
        result = play()
    elif args.command == "pause":
        result = pause()
    elif args.command == "crossfade":
        result = crossfade(args.value)
    elif args.command == "echo":
        result = echo()
    elif args.command == "send-custom-cc":
        result = send_custom_cc(args.control, args.value)
    else:
        raise RuntimeError(f"Unknown command: {args.command}")

    print(json.dumps({"ok": True, "result": result}))


if __name__ == "__main__":
    main()