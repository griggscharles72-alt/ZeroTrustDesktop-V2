from ztd.state import collect_runtime_state, diff_states


def test_collect_runtime_state_shape() -> None:
    state = collect_runtime_state()
    assert state.repo_root
    assert state.git_branch
    assert state.git_commit
    assert state.python_executable
    assert state.python_version


def test_diff_states_initial() -> None:
    current = {
        "timestamp_utc": "2026-03-14T00:00:00Z",
        "git_commit": "abc123",
    }
    diff_payload = diff_states(None, current)
    assert diff_payload["status"] == "initial_state"
    assert "git_commit" in diff_payload["changed_keys"]


def test_diff_states_changed() -> None:
    previous = {
        "timestamp_utc": "2026-03-14T00:00:00Z",
        "git_commit": "abc123",
    }
    current = {
        "timestamp_utc": "2026-03-14T00:01:00Z",
        "git_commit": "def456",
    }
    diff_payload = diff_states(previous, current)
    assert diff_payload["status"] == "changed"
    assert diff_payload["changed_count"] >= 1
