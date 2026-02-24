import subprocess
import sys

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


def main(argv: list[str] | None = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python -m dual_jbl_sound <command>")
        print("Commands:")
        print("  list-sinks")
        sys.exit(1)

    command = argv[0]

    if command == "list-sinks":
        list_sinks()
        return

    print(f"Unknow command: {command}", file=sys.stderr)
    sys.exit(1)
