from dk_tracker.ui import selfcheck


def test_selfcheck_loads_the_real_main_window(qapp):
    report = selfcheck.run()
    assert report[0].startswith("PySide6 ")
    assert "from QML" in report[1]
    assert report[2].startswith("layer-shell-qt: ")


def test_selfcheck_reports_a_failure_with_exit_code_1(monkeypatch, capsys):
    def broken():
        raise ImportError("undefined symbol: _ZN14QObjectPrivateC2E16QtPrivate_6_11_2")

    monkeypatch.setattr(selfcheck, "run", broken)
    assert selfcheck.main() == 1
    assert "FAILED: ImportError" in capsys.readouterr().err
