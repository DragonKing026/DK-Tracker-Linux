"""Settings (F-01, F-13, F-21, F-22): an ordinary window with a frame, not a layer surface.

The token field starts empty. A token already in the wallet stays there unless a new one is
typed, so the token is never read back into a widget (spec, section 8).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from dk_tracker.core.settings import Settings

LANGUAGES = (("auto", "optLangAuto"), ("pl", "optLangPl"), ("en", "optLangEn"))


class SettingsDialog(QDialog):
    saveRequested = Signal(object, object)  # Settings, new token or None to keep the stored one
    testRequested = Signal(str, str)  # address, token as typed ("" = the stored one)

    def __init__(self, t: Callable[..., str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(480)
        self._t = t
        self._loaded = Settings()
        self._has_token = False
        self._secrets_problem: str | None = None

        self.url = QLineEdit()
        self.token = QLineEdit()
        self.token.setEchoMode(QLineEdit.EchoMode.Password)
        self.token_hint = QLabel()  # one line: top-level windows ignore height-for-width
        self.language = QComboBox()
        for code, _key in LANGUAGES:
            self.language.addItem("", code)
        self.min_description = QSpinBox(minimum=0, maximum=200)
        self.min_hint = QLabel()  # one line: top-level windows ignore height-for-width
        self.long_timer = QDoubleSpinBox(minimum=0.0, maximum=24.0, singleStep=0.5, decimals=1)
        self.long_hint = QLabel()  # one line: top-level windows ignore height-for-width
        self.notify_connection = QCheckBox()
        self.notify_menu = QCheckBox()
        self.autostart = QCheckBox()
        self.show_tray = QCheckBox()
        self.warning = QLabel(wordWrap=True)
        self.status = QLabel(wordWrap=True)
        self.test_button = QPushButton()
        self.save_button = QPushButton()
        self.save_button.setDefault(True)
        self.close_button = QPushButton()

        # A grid, not a QFormLayout: the form layout cut wrapped hints to one line.
        self.form = QGridLayout()
        self.form.setColumnStretch(1, 1)
        self._labels = {name: QLabel() for name in ("url", "token", "language", "min", "long")}
        rows = (
            ("url", self.url, None),
            ("token", self.token, self.token_hint),
            ("language", self.language, None),
            ("min", self.min_description, self.min_hint),
            ("long", self.long_timer, self.long_hint),
        )
        row = 0
        for name, field, hint in rows:
            self._labels[name].setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.form.addWidget(self._labels[name], row, 0)
            self.form.addWidget(field, row, 1)
            row += 1
            if hint is not None:
                self.form.addWidget(hint, row, 1)
                row += 1
        buttons = QHBoxLayout()
        buttons.addWidget(self.test_button)
        buttons.addStretch(1)
        buttons.addWidget(self.close_button)
        buttons.addWidget(self.save_button)
        layout = QVBoxLayout(self)
        # The window may not get smaller than its content: wrapped hints were cut off.
        layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        layout.addLayout(self.form)
        for box in (self.notify_connection, self.notify_menu, self.autostart, self.show_tray):
            layout.addWidget(box)
        layout.addWidget(self.warning)
        layout.addWidget(self.status)
        layout.addLayout(buttons)

        self.url.textChanged.connect(lambda _text: self._paint_warning())
        self.test_button.clicked.connect(self._on_test)
        self.save_button.clicked.connect(self._on_save)
        self.close_button.clicked.connect(self.reject)
        self.warning.hide()
        self.status.hide()
        self.retranslate(t)

    def load(self, settings: Settings, *, has_token: bool) -> None:
        self._loaded = settings
        self._has_token = has_token
        self.url.setText(settings.url)
        self.token.clear()
        self.language.setCurrentIndex(max(0, self.language.findData(settings.language)))
        self.min_description.setValue(settings.min_description)
        self.long_timer.setValue(settings.long_timer_hours)
        self.notify_connection.setChecked(settings.notify_connection)
        self.notify_menu.setChecked(settings.notify_menu_actions)
        self.autostart.setChecked(settings.autostart)
        self.show_tray.setChecked(settings.show_tray)
        self.status.hide()
        self.retranslate(self._t)

    def set_secrets_problem(self, key: str | None) -> None:
        self._secrets_problem = key
        self._paint_warning()

    def show_status(self, text: str, *, ok: bool) -> None:
        self.status.setText(text)
        self.status.setProperty("ok", "true" if ok else "false")
        self.status.setStyleSheet(f"color: {'#16a34a' if ok else '#dc2626'};")
        self.status.setVisible(bool(text))

    def set_busy(self, busy: bool) -> None:
        self.save_button.setEnabled(not busy)
        self.test_button.setEnabled(not busy)

    def retranslate(self, t: Callable[..., str]) -> None:
        self._t = t
        self.setWindowTitle(t("optTitle"))
        self._labels["url"].setText(t("optUrl"))
        self._labels["token"].setText(t("optToken"))
        self._labels["language"].setText(t("optLang"))
        self._labels["min"].setText(t("optMinDesc"))
        self._labels["long"].setText(t("optLongTimer"))
        self.url.setPlaceholderText(t("optUrlHint"))
        self.token.setPlaceholderText(t("optTokenKeep") if self._has_token else "")
        self.token_hint.setText(t("optTokenHint"))
        for index, (_code, key) in enumerate(LANGUAGES):
            self.language.setItemText(index, t(key))
        self.min_hint.setText(t("optMinDescHint"))
        self.long_hint.setText(t("optLongTimerHint"))
        self.notify_connection.setText(t("optNotifyConnection"))
        self.notify_menu.setText(t("optNotifyMenu"))
        self.autostart.setText(t("optAutostart"))
        self.show_tray.setText(t("optShowTray"))
        self.test_button.setText(t("optTest"))
        self.save_button.setText(t("optSave"))
        self.close_button.setText(t("optClose"))
        self._paint_warning()

    def current(self) -> Settings:
        return replace(
            self._loaded,
            url=self.url.text(),
            language=self.language.currentData(),
            min_description=self.min_description.value(),
            long_timer_hours=self.long_timer.value(),
            notify_connection=self.notify_connection.isChecked(),
            notify_menu_actions=self.notify_menu.isChecked(),
            autostart=self.autostart.isChecked(),
            show_tray=self.show_tray.isChecked(),
        ).normalized()

    def _on_test(self) -> None:
        self.show_status(self._t("optTesting"), ok=True)
        self.testRequested.emit(self.url.text().strip().rstrip("/"), self.token.text().strip())

    def _on_save(self) -> None:
        settings = self.current()
        token = self.token.text().strip()
        if not settings.url:
            self.show_status(self._t("optUrlRequired"), ok=False)
            return
        if not token and not self._has_token:
            self.show_status(self._t("optTokenRequired"), ok=False)
            return
        self.saveRequested.emit(settings, token or None)

    def _paint_warning(self) -> None:
        notes = [self._t(key) for key in replace(self._loaded, url=self.url.text()).warnings()]
        if self._secrets_problem:
            notes.append(self._t(self._secrets_problem))
        self.warning.setText("\n\n".join(notes))
        self.warning.setVisible(bool(notes))
