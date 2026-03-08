import importlib
import sys

import pytest


def load_main_module(monkeypatch, startup_inputs=None):
    """
    Import Main.py safely by patching input/os.system before import.

    Main.py executes main_menu(...) at import time, so we need to provide
    enough mocked input values for that startup path.
    """
    if startup_inputs is None:
        startup_inputs = ["1"]

    inputs = iter(startup_inputs)

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    sys.modules.pop("Main", None)
    return importlib.import_module("Main")


def test_dispatch_table_contains_settings_command_only(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    assert "settings" in main.dispatch_table
    assert main.dispatch_table["settings"] is main.settings
    assert len(main.dispatch_table) == 1


@pytest.mark.parametrize(("user_input", "expected"), [("1", 1), ("2", 2), ("3", 3)])
def test_main_menu_returns_selected_difficulty(monkeypatch, user_input, expected):
    main = load_main_module(monkeypatch, ["1"])

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: user_input)
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    assert main.main_menu("startup") == expected


def test_main_menu_executes_settings_command(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    calls = {"count": 0}

    def fake_settings(sound_enabled=None):
        calls["count"] += 1
        return sound_enabled

    monkeypatch.setattr(main, "settings", fake_settings)
    main.dispatch_table["settings"] = main.settings
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "settings")
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    result = main.main_menu("startup")

    assert result is None
    assert calls["count"] == 1


def test_main_menu_prints_error_for_unknown_command(monkeypatch, capsys):
    main = load_main_module(monkeypatch, ["1"])

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "unknown-command")
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    result = main.main_menu("startup")
    captured = capsys.readouterr()

    assert result is None
    assert "Command not recognised." in captured.out


def test_main_menu_quit_raises_system_exit(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "q")
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    with pytest.raises(SystemExit):
        main.main_menu("startup")


def test_main_menu_return_raises_system_exit_when_invoked_ingame(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "r")
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    with pytest.raises(SystemExit):
        main.main_menu("ingame")


def test_settings_sound_option_disable_returns_false(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    inputs = iter(["2", "y", "", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    assert main.settings() is False


def test_settings_sound_option_enable_returns_true(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    inputs = iter(["2", "n", "", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    assert main.settings() is True


def test_settings_return_option_returns_current_sound_state(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "R")
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    assert main.settings() is None


def test_settings_invalid_sound_choice_then_return_keeps_existing_value(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    inputs = iter(["2", "maybe", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    assert main.settings(True) is True