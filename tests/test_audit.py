from ztd.audit import build_audit_summary, collect_audit


def test_collect_audit_returns_items() -> None:
    items = collect_audit()
    assert len(items) > 0


def test_audit_contains_project_mode() -> None:
    items = collect_audit()
    names = {item.name for item in items}
    assert "config.project_mode" in names


def test_audit_contains_apply_restore_guards() -> None:
    items = collect_audit()
    names = {item.name for item in items}
    assert "config.allow_apply" in names
    assert "config.allow_restore" in names


def test_audit_summary_exists() -> None:
    items = collect_audit()
    summary = build_audit_summary(items)
    assert "ok_count" in summary
    assert "warn_count" in summary
    assert "critical_warn_count" in summary
    assert "result" in summary


def test_audit_result_is_baseline_safe() -> None:
    items = collect_audit()
    summary = build_audit_summary(items)
    assert summary["result"] == "baseline_safe"
