import argparse
import json

from dj.commands import (
    add_to_automix_next,
    add_to_sidelist,
    crossfade,
    crossfade_auto,
    crossfade_center,
    crossfade_left,
    crossfade_right,
    deck_play_pause,
    echo,
    list_results,
    load_deck,
    ping_cc_range,
    ping_note_range,
    search_library,
    search_load,
    search_select,
    select_result,
    send_custom_cc,
    send_custom_note,
    start_automix,
)
from dj.midi import get_output_names, test_connection


def main() -> None:
    parser = argparse.ArgumentParser(description="VirtualDJ skill runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("healthcheck")
    subparsers.add_parser("list-outputs")
    subparsers.add_parser("test-connection")
    subparsers.add_parser("echo")
    subparsers.add_parser("add-to-sidelist")
    subparsers.add_parser("automix-start")
    subparsers.add_parser("automix-add-next")

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

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query", type=str)
    search_parser.add_argument("--app", type=str, default="VirtualDJ")
    search_parser.add_argument("--no-shortcut", action="store_true")
    search_parser.add_argument("--no-submit", action="store_true")

    list_results_parser = subparsers.add_parser("list-results")
    list_results_parser.add_argument("query", type=str)
    list_results_parser.add_argument("--limit", type=int, default=10)
    list_results_parser.add_argument("--database", type=str, default=None)

    select_result_parser = subparsers.add_parser("select-result")
    select_result_parser.add_argument("index", type=int)
    select_result_parser.add_argument("--app", type=str, default="VirtualDJ")
    select_result_parser.add_argument("--no-reset", action="store_true")

    load_deck_parser = subparsers.add_parser("load-deck")
    load_deck_parser.add_argument("--deck", type=int, required=True, choices=[1, 2])

    search_select_parser = subparsers.add_parser("search-select")
    search_select_parser.add_argument("query", type=str)
    search_select_parser.add_argument("--result", type=int, default=1)
    search_select_parser.add_argument("--app", type=str, default="VirtualDJ")

    search_load_parser = subparsers.add_parser("search-load")
    search_load_parser.add_argument("query", type=str)
    search_load_parser.add_argument("--deck", type=int, required=True, choices=[1, 2])
    search_load_parser.add_argument("--result", type=int, default=1)
    search_load_parser.add_argument("--app", type=str, default="VirtualDJ")

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
    elif args.command == "add-to-sidelist":
        result = add_to_sidelist()
    elif args.command == "automix-start":
        result = start_automix()
    elif args.command == "automix-add-next":
        result = add_to_automix_next()
    elif args.command == "send-custom-cc":
        result = send_custom_cc(args.control, args.value)
    elif args.command == "send-custom-note":
        result = send_custom_note(args.note, args.velocity)
    elif args.command == "ping-note-range":
        result = ping_note_range(args.start, args.end)
    elif args.command == "ping-cc-range":
        result = ping_cc_range(args.start, args.end, args.value)
    elif args.command == "search":
        result = search_library(
            args.query,
            app_name=args.app,
            no_shortcut=args.no_shortcut,
            no_submit=args.no_submit,
        )
    elif args.command == "list-results":
        result = list_results(args.query, limit=args.limit, database_xml=args.database)
    elif args.command == "select-result":
        result = select_result(
            args.index,
            app_name=args.app,
            no_reset=args.no_reset,
        )
    elif args.command == "load-deck":
        result = load_deck(args.deck)
    elif args.command == "search-select":
        result = search_select(
            args.query,
            result_index=args.result,
            app_name=args.app,
        )
    elif args.command == "search-load":
        result = search_load(
            args.query,
            deck=args.deck,
            result_index=args.result,
            app_name=args.app,
        )
    else:
        raise RuntimeError(f"Unknown command: {args.command}")

    print(json.dumps({"ok": True, "result": result}))


if __name__ == "__main__":
    main()
