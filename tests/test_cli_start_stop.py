from unittest.mock import patch

from dual_jbl_sound.cli import main


@patch("dual_jbl_sound.cli.ConfigStore")
def test_start_mono_saves_config(MockStore):
    store = MockStore.return_value

    main(["start", "--mode", "mono", "--a", "AAA", "--b", "BBB"])

    store.save.assert_called_once()
    saved = store.save.call_args.args[0]
    assert saved["mode"] == "mono"
    assert saved["a_query"] == "AAA"
    assert saved["b_query"] == "BBB"


@patch("dual_jbl_sound.cli.ConfigStore")
def test_start_lr_saves_config(MockStore):
    store = MockStore.return_value

    main(["start", "--mode", "lr", "--left", "L", "--right", "R"])

    saved = store.save.call_args.args[0]
    assert saved["mode"] == "lr"
    assert saved["left_query"] == "L"
    assert saved["right_query"] == "R"


@patch("dual_jbl_sound.cli.ConfigStore")
def test_stop_clears_config(MockStore):
    store = MockStore.return_value

    main(["stop"])

    store.clear.assert_called_once()
