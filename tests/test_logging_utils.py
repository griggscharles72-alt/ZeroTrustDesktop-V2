from ztd.logging_utils import get_log_file_path, get_logger


def test_log_file_path_location() -> None:
    path = get_log_file_path()
    assert path.name == "ztd.log"
    assert path.parent.name == "logs"


def test_get_logger_returns_named_logger() -> None:
    logger = get_logger("ztd.test_logging")
    assert logger.name == "ztd.test_logging"
    assert len(logger.handlers) >= 2
