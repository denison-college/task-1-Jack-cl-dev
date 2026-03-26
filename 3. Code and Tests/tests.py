import importlib
import sys
import pytest
from tinydb import TinyDB

def load_main_module(monkeypatch, startup_inputs=None):
    """
    Import main.py safely by patching input/os.system before import.

    main.py executes main_menu(...) at import time, so we need to provide
    enough mocked input values for that startup path.
    """
    if startup_inputs is None:
        startup_inputs = ["1"]

    inputs = iter(startup_inputs)

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    sys.modules.pop("Main", None)
    return importlib.import_module("Main")


def test_dispatch_table_contains_expected_commands(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    assert set(main.dispatch_table) == {"settings", "debug"}
    assert main.dispatch_table["settings"] is main.settings
    assert callable(main.dispatch_table["debug"])


@pytest.mark.parametrize(("user_input", "expected"), [("1", 1), ("2", 2), ("3", 3)])
def test_main_menu_returns_selected_difficulty(monkeypatch, user_input, expected):
    main = load_main_module(monkeypatch, ["1"])

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: user_input)
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    assert main.main_menu("startup") == expected


def test_main_menu_executes_settings_command(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    calls = {"count": 0}

    def fake_settings():
        calls["count"] += 1

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


def test_settings_returns_none_when_return_selected(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "R")
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    assert main.settings() is None


def test_settings_sound_option_enable_updates_state(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    inputs = iter(["2", "y", "", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    original = main.sound_enabled
    result = main.settings()

    assert result is None
    assert main.sound_enabled is True
    assert main.sound_enabled != original or original is True


def test_settings_sound_option_disable_updates_state(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    inputs = iter(["2", "n", "", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    original = main.sound_enabled
    result = main.settings()

    assert result is None
    assert main.sound_enabled is False
    assert main.sound_enabled != original or original is False


def test_settings_invalid_sound_choice_then_return_keeps_existing_value(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    original = main.sound_enabled
    inputs = iter(["2", "maybe", "", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    main.settings()

    assert main.sound_enabled is original


def test_settings_colour_option_can_update_colour(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    inputs = iter(["1", "background", "navy", "", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    main.settings()

    assert main.game_colours["background"] == "navy"


def test_settings_symbol_option_can_update_symbol(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    inputs = iter(["3", "flag_symbol", "F", "", "R"])
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(inputs))
    monkeypatch.setattr("os.system", lambda *args, **kwargs: 0)

    main.settings()

    assert main.game_settings["flag_symbol"] == "F"


def test_database_file_loads_and_contains_expected_game_data(monkeypatch):
    main = load_main_module(monkeypatch, ["1"])

    assert main.db.all(), "Database should not be empty"
    record = main.db.all()[0]

    assert "settings" in record
    assert "colours" in record
    assert "sound_enabled" in record
    assert record["settings"]["flag_symbol"] == "X"
    assert record["settings"]["mine symbol"] == "O"
    assert isinstance(record["sound_enabled"], bool)
    assert record["colours"]["background"] == "black"


def test_database_file_loads_and_main_reuses_existing_data_without_inserting_defaults(monkeypatch):
    before_db = TinyDB("db.json")
    before_records = before_db.all()
    before_count = len(before_records)

    assert before_count > 0, "db.json should already contain at least one record"

    expected_record = {
        "settings": {"flag_symbol": "X", "mine symbol": "O"},
        "colours": {
            "background": "black",
            "text": "white",
            "flag": "red",
            "mine": "green",
            "title": "yellow",
            "mine_count": "blue",
            "timer_colour": "magenta",
        },
        "sound_enabled": True,
    }

    assert expected_record in before_records

    main = load_main_module(monkeypatch, ["1"])

    after_db = main.db
    after_records = after_db.all()
    after_count = len(after_records)

    assert after_count == before_count
    assert expected_record in after_records
    assert after_records[0]["settings"] == expected_record["settings"]
    assert after_records[0]["colours"] == expected_record["colours"]
    assert after_records[0]["sound_enabled"] is True