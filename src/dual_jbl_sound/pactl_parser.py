from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AudioSink:
    id: int
    name: str
    driver: str
    format: str
    state: str


def parse_pactl_list_short_sinks(text: str) -> list[AudioSink]:
    """
    Parse `pactl list short sinks` output.

    Expected format per line (tab-separated):
        <id>    <name>  <driver>    <format>    <state>

    Example:
        59  alsa_output...  PipeWire  s32le 2ch 48000Hz  SUSPENDED
    """
    sinks: list[AudioSink] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) < 5:
            # If output format changes, fail fast with a readable error.
            raise ValueError(f"Unexpected pactl line format: {raw_line!r}")

        sink_id_str, name, driver, fmt, state = parts[:5]
        sinks.append(
            AudioSink(
                id=int(sink_id_str),
                name=name,
                driver=driver,
                format=fmt,
                state=state,
            )
        )

    return sinks
