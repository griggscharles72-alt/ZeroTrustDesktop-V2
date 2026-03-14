from ztd.observe import collect_observation


def test_collect_observation_returns_items() -> None:
    items = collect_observation()
    assert len(items) > 0


def test_observe_contains_age_fields() -> None:
    items = collect_observation()
    names = {item.name for item in items}
    assert "latest_doctor_snapshot_age" in names
    assert "latest_doctor_report_age" in names


def test_observe_contains_timestamp_fields() -> None:
    items = collect_observation()
    names = {item.name for item in items}
    assert "latest_doctor_snapshot_timestamp" in names
    assert "latest_doctor_report_timestamp" in names
