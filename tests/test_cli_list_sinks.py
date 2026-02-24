from unittest.mock import Mock, patch

from dual_jbl_sound.cli import main

MOCK_PACTL_OUTPUT = """\
59\talsa_output.pci-0000_04_00.6.analog-stereo\tPipeWire\ts32le 2ch 48000Hz\tSUSPENDED
77\talsa_output.pci-0000_04_00.1.hdmi-stereo\tPipeWire\ts32le 2ch 48000Hz\tRUNNING
"""


@patch("dual_jbl_sound.cli.subprocess.run")
def test_list_sinks_prints_table(mock_run, capsys):
    mock_process = Mock()
    mock_process.stdout = MOCK_PACTL_OUTPUT
    mock_process.returncode = 0
    mock_run.return_value = mock_process

    main(["list-sinks"])

    captured = capsys.readouterr()
    assert "ID" in captured.out
    assert "STATE" in captured.out
    assert "alsa_output.pci-0000_04_00.6.analog-stereo" in captured.out
    assert "RUNNING" in captured.out
