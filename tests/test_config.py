from ztd.config import load_config


def test_config_loads() -> None:
    cfg = load_config()
    assert isinstance(cfg, dict)


def test_expected_top_level_keys_exist() -> None:
    cfg = load_config()
    for key in (
        "project",
        "runtime",
        "launcher",
        "safety",
        "network",
        "firewall",
        "observability",
        "doctor",
    ):
        assert key in cfg


def test_safety_defaults_are_false() -> None:
    cfg = load_config()
    assert cfg["safety"]["allow_apply"] is False
    assert cfg["safety"]["allow_restore"] is False
