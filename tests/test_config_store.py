from pathlib import Path

from dual_jbl_sound.config_store import ConfigStore


def test_config_store_roundtrip(tmp_path: Path):
    store = ConfigStore(base_dir=tmp_path)

    data = {"mode": "mono", "a_query": "AAA", "b_query": "BBB"}
    store.save(data)

    loaded = store.load()
    assert loaded == data


def test_config_store_load_returns_none_if_missing(tmp_path: Path):
    store = ConfigStore(base_dir=tmp_path)
    assert store.load() is None
