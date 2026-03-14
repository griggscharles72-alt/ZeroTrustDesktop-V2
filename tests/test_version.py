from ztd.version import FULL_VERSION, PHASE, PROJECT_NAME, VERSION, get_version


def test_project_name() -> None:
    assert PROJECT_NAME == "ZeroTrustDesktop-V2"


def test_version_string() -> None:
    assert VERSION == "0.1.1"


def test_phase_string() -> None:
    assert PHASE == "read-only baseline"


def test_full_version() -> None:
    assert FULL_VERSION == "ZeroTrustDesktop-V2 0.1.1 (read-only baseline)"
    assert get_version() == FULL_VERSION
