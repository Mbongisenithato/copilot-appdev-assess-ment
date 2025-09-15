import pytest
from unittest.mock import patch
from src.reminder_app import send_reminder, is_valid_email, main

def test_send_print_reminder(capsys):
    send_reminder("Test message")
    captured = capsys.readouterr()
    assert "Test message" in captured.out

def test_send_email_invalid_format(caplog):
    send_reminder("Test message", method="email", email="not-an-email")
    assert "Invalid email format." in caplog.text

def test_send_email_missing_address(caplog):
    send_reminder("Test message", method="email", email=None)
    assert "Invalid method or missing email address." in caplog.text

def test_is_valid_email():
    assert is_valid_email("user@example.com")
    assert not is_valid_email("invalid-email")

def test_invalid_interval(monkeypatch):
    test_args = ["reminder_app.py", "--interval", "0"]
    monkeypatch.setattr("sys.argv", test_args)
    with pytest.raises(SystemExit):
        main()

def test_main_loop_mocked():
    with patch("schedule.run_pending") as mock_run, patch("time.sleep") as mock_sleep:
        mock_run.side_effect = [None, None, KeyboardInterrupt()]
        mock_sleep.side_effect = lambda x: None
        with pytest.raises(KeyboardInterrupt):
            from src.reminder_app import run_scheduler
            run_scheduler()