from ztd.paths import get_paths


def test_paths_exist() -> None:
    paths = get_paths()
    assert paths.repo_root.exists()
    assert paths.config_dir.exists()
    assert paths.output_dir.exists()
    assert paths.reports_dir.exists()
    assert paths.snapshots_dir.exists()
    assert paths.diffs_dir.exists()
    assert paths.logs_dir.exists()
    assert paths.state_dir.exists()


def test_key_files_exist() -> None:
    paths = get_paths()
    assert paths.default_config_file.exists()
    assert paths.local_config_file.exists()
