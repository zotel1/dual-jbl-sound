import pytest

from dual_jbl_sound.pactl_parser import AudioSink
from dual_jbl_sound.targets import TargetSelectionError, select_targets


def _sink(id_: int, name: str) -> AudioSink:
    return AudioSink(
        id=id_,
        name=name,
        driver="PipeWire",
        format="s32le 2ch 48000Hz",
        state="RUNNING",
    )


def test_select_targets_by_exact_name():
    sinks = [
        _sink(1, "alsa_output.pci-0000_04_00.6.analog-stereo"),
        _sink(2, "bluez_output.AA_BB_CC_DD_EE_FF.a2dp-sink"),  # JBL 1 (ej)
        _sink(3, "bluez_output.11_22_33_44_55_66.a2dp-sink"),  # JBL 2 (ej)
    ]

    left, right = select_targets(
        sinks,
        left_query="bluez_output.AA_BB_CC_DD_EE_FF.a2dp-sink",
        right_query="bluez_output.11_22_33_44_55_66.a2dp-sink",
    )

    assert left.id == 2
    assert right.id == 3


def test_select_targets_by_substring():
    sinks = [
        _sink(2, "bluez_output.AA_BB_CC_DD_EE_FF.a2dp-sink"),
        _sink(3, "bluez_output.11_22_33_44_55_66.a2dp-sink"),
    ]

    left, right = select_targets(
        sinks,
        left_query="AA_BB_CC_DD_EE_FF",
        right_query="11_22_33_44_55_66",
    )

    assert left.id == 2
    assert right.id == 3


def test_select_targets_raises_if_not_found():
    sinks = [_sink(2, "bluez_output.AA_BB_CC_DD_EE_FF.a2dp-sink")]

    with pytest.raises(TargetSelectionError):
        select_targets(
            sinks,
            left_query="does-not-exist",
            right_query="AA_BB_CC_DD_EE_FF",
        )


def test_select_targets_raises_if_same_sink_selected_twice():
    sinks = [
        _sink(2, "bluez_output.AA_BB_CC_DD_EE_FF.a2dp-sink"),
        _sink(3, "bluez_output.11_22_33_44_55_66.a2dp-sink"),
    ]

    with pytest.raises(TargetSelectionError):
        select_targets(
            sinks,
            left_query="AA_BB_CC_DD_EE_FF",
            right_query="AA_BB_CC_DD_EE_FF",
        )
