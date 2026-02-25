from __future__ import annotations

from dual_jbl_sound.pactl_parser import AudioSink


class TargetSelectionError(Exception):
    pass


def _match_one(sinks: list[AudioSink], query: str) -> AudioSink:
    # 1) match exact
    for s in sinks:
        if s.name == query:
            return s

    # 2) match substring
    matches = [s for s in sinks if query in s.name]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(m.name for m in matches)
        raise TargetSelectionError(f"Query '{query}' is ambiguous. Matches: {names}")

    raise TargetSelectionError(f"Query '{query}' did not match any sink.")


def select_targets(
    sinks: list[AudioSink],
    left_query: str,
    right_query: str,
) -> tuple[AudioSink, AudioSink]:
    left = _match_one(sinks, left_query)
    right = _match_one(sinks, right_query)

    if left.id == right.id:
        raise TargetSelectionError("Left and right targets must be different sinks.")

    return left, right
