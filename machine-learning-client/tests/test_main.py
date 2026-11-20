"""Placeholder tests for the ML client"""

from main import main


def test_main_prints_message(capsys):
    """main() should print its startup message"""
    main()
    captured = (
        capsys.readouterr()
    )  # capsys can read text written to stdout/stderr, so our print() statement
    assert "ML client is running" in captured.out
