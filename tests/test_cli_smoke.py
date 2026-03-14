from ztd.cli import run_command


def test_doctor_runs() -> None:
    assert run_command("doctor") == 0


def test_status_runs() -> None:
    assert run_command("status") == 0


def test_audit_runs() -> None:
    assert run_command("audit") == 0


def test_observe_runs() -> None:
    assert run_command("observe") == 0


def test_apply_refuses_by_default() -> None:
    assert run_command("apply") == 1


def test_restore_refuses_by_default() -> None:
    assert run_command("restore") == 1
