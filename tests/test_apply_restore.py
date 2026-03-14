from ztd.apply import collect_apply_preview, run_apply
from ztd.restore import collect_restore_preview, run_restore


def test_apply_preview_shape() -> None:
    preview = collect_apply_preview()
    assert preview.summary == "preview_only_no_state_change"
    assert preview.would_write_firewall is True
    assert preview.would_write_restore_state is True
    assert preview.would_enforce_runtime is True


def test_restore_preview_shape() -> None:
    preview = collect_restore_preview()
    assert preview.summary == "preview_only_no_state_change"
    assert preview.would_restore_firewall is True
    assert preview.would_restore_runtime is True
    assert preview.would_load_saved_state is True


def test_apply_still_refuses_by_default() -> None:
    assert run_apply() == 1


def test_restore_still_refuses_by_default() -> None:
    assert run_restore() == 1
