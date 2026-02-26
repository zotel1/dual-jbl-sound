import argparse
import subprocess
import sys

from dual_jbl_sound.config_store import ConfigStore
from dual_jbl_sound.pactl_parser import parse_pactl_list_short_sinks


def list_sinks() -> None:
    result = subprocess.run(
        ["pactl", "list", "short", "sinks"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print("Error: could not run 'pactl list short sinks'", file=sys.stderr)
        sys.exit(1)

    sinks = parse_pactl_list_short_sinks(result.stdout)

    print(f"{'ID':<5} {'STATE':<10} NAME")
    print("-" * 60)
    for sink in sinks:
        print(f"{sink.id:<5} {sink.state:<10} {sink.name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dual-jbl-sound")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-sinks")

    start = sub.add_parser("start")
    start.add_argument("--mode", choices=["mono", "lr"], required=True)

    # mono
    start.add_argument("--a")
    start.add_argument("--b")

    # lr
    start.add_argument("--left")
    start.add_argument("--right")

    sub.add_parser("stop")
    return parser


def cmd_start(args: argparse.Namespace) -> None:
    store = ConfigStore()

    if args.mode == "mono":
        if not args.a or not args.b:
            raise SystemExit("start --mode mono requires --a and --b")
        store.save({"mode": "mono", "a_query": args.a, "b_query": args.b})
        print("Saved config: mode=mono")
        return

    if args.mode == "lr":
        if not args.left or not args.right:
            raise SystemExit("start --mode lr requires --left and --right")
        store.save({"mode": "lr", "left_query": args.left, "right_query": args.right})
        print("Saved config: mode=lr")
        return

    raise SystemExit(f"Unsupported mode: {args.mode}")


def cmd_stop() -> None:
    store = ConfigStore()
    store.clear()
    print("Cleared config")


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list-sinks":
        list_sinks()
        return

    if args.command == "start":
        cmd_start(args)
        return

    if args.command == "stop":
        cmd_stop()
        return

    raise SystemExit(1)
