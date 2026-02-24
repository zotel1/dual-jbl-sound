from dual_jbl_sound.pactl_parser import parse_pactl_list_short_sinks

PACTL_OUTPUT = """\
59\talsa_output.pci-0000_04_00.6.analog-stereo\tPipeWire\ts32le 2ch 48000Hz\tSUSPENDED
77\talsa_output.pci-0000_04_00.1.hdmi-stereo\tPipeWire\ts32le 2ch 48000Hz\tRUNNING
"""


def test_parse_pactl_list_short_sinks_parses_rows():
    sinks = parse_pactl_list_short_sinks(PACTL_OUTPUT)

    assert len(sinks) == 2

    assert sinks[0].id == 59
    assert sinks[0].name == "alsa_output.pci-0000_04_00.6.analog-stereo"
    assert sinks[0].driver == "PipeWire"
    assert sinks[0].format == "s32le 2ch 48000Hz"
    assert sinks[0].state == "SUSPENDED"

    assert sinks[1].id == 77
    assert sinks[1].name == "alsa_output.pci-0000_04_00.1.hdmi-stereo"
    assert sinks[1].state == "RUNNING"


def test_parse_pactl_list_short_sinks_ignores_empty_lines():
    sinks = parse_pactl_list_short_sinks(PACTL_OUTPUT + "\n\n")
    assert len(sinks) == 2
