import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from dk_tracker.ui.icons import GLYPHS, glyph, tray_icon, tray_pixmap
from dk_tracker.ui.theme import DARK, LIGHT, palette_for, stylesheet


def test_palettes_match_the_add_on():
    assert (LIGHT["bg"], DARK["bg"]) == ("#ffffff", "#16181d")
    assert set(LIGHT) == set(DARK)
    assert LIGHT["start"] == DARK["start"] == "#16a34a"


def test_scheme_is_taken_from_qt_or_from_the_window_colour():
    assert palette_for(Qt.ColorScheme.Dark, QColor("#ffffff")) is DARK
    assert palette_for(Qt.ColorScheme.Light, QColor("#000000")) is LIGHT
    assert palette_for(Qt.ColorScheme.Unknown, QColor("#202326")) is DARK
    assert palette_for(Qt.ColorScheme.Unknown, QColor("#eff0f1")) is LIGHT


def test_stylesheet_uses_the_palette():
    css = stylesheet(DARK)
    assert "#16181d" in css and "#e02f2f" in css
    assert "#ffffff" not in stylesheet(DARK).replace("color: #ffffff", "")  # white only as text on buttons


def centre(image):
    return QColor(image.pixel(image.width() // 2, image.height() // 2))


def edge(image):
    return QColor(image.pixel(image.width() // 2, 2))


@pytest.mark.parametrize(
    ("kind", "label", "colour"), [("running", "1:22", "#16a34a"), ("error", "!", "#dc2626")]
)
def test_badge_background_has_the_state_colour(qapp, kind, label, colour):
    image = tray_pixmap(kind, label, 44).toImage()
    assert edge(image).name() == colour


def test_idle_and_unconfigured_draw_a_grey_clock(qapp):
    for kind in ("idle", "unconfigured"):
        assert edge(tray_pixmap(kind, "", 44).toImage()).name() == "#6b7280"


def test_label_changes_the_picture(qapp):
    assert tray_pixmap("running", "47m", 22).toImage() != tray_pixmap("running", "48m", 22).toImage()


def test_tray_icon_has_every_panel_size(qapp):
    sizes = {size.width() for size in tray_icon("running", "47m").availableSizes()}
    assert {16, 22, 24, 32, 44, 64} <= sizes


def test_glyphs_render_in_the_given_colour(qapp):
    for name in GLYPHS:
        assert not glyph(name, "#16a34a").isNull(), name
    image = glyph("stop", "#ffffff", 20).pixmap(20, 20).toImage()
    assert centre(image).name() == "#ffffff"


def test_app_icon_is_our_own_ws_tile_not_the_kimai_logo(qapp):
    """Kimai's trademark policy: no impression of being an official Kimai app (0063)."""
    from dk_tracker.ui.icons import app_icon

    icon = app_icon()
    assert not icon.isNull()
    image = icon.pixmap(64, 64).toImage()
    ring = QColor(image.pixel(32, 13))  # top of the green progress ring (inside the 8 % margin)
    tile = QColor(image.pixel(20, 32))  # dark tile between the ring and the letters
    assert ring.green() > 150 and ring.red() < 100
    assert max(tile.red(), tile.green(), tile.blue()) < 90


@pytest.mark.parametrize("label", ["0m", "47m", "1:22", "12:05"])
def test_badge_text_keeps_a_margin_from_the_edge(qapp, label):
    image = tray_pixmap("running", label, 44).toImage()
    margin = 5  # ~12 % of the icon
    for x in list(range(margin)) + list(range(44 - margin, 44)):
        for y in range(44):
            colour = QColor(image.pixel(x, y))
            assert not (colour.red() > 200 and colour.green() > 200 and colour.blue() > 200), (label, x, y)


def test_combo_arrows_are_drawn_from_our_own_svg(tmp_path):
    from pathlib import Path

    from dk_tracker.ui.theme import write_assets

    assets = write_assets(DARK, tmp_path)
    css = stylesheet(DARK, assets)
    for name in ("chevron", "chevron_disabled"):
        assert Path(assets[name]).read_text().startswith("<svg")
        assert assets[name] in css
    assert "QComboBox::down-arrow" in css


def test_scroll_bars_are_thin_without_arrow_buttons():
    css = stylesheet(DARK)
    assert "QScrollBar::add-line:vertical" in css and "height: 0" in css


def test_billable_states_stand_out():
    css = stylesheet(DARK)
    assert '#rowBillable[on="true"]' in css
    assert '#billable[on="false"]' in css and DARK["muted"] in css


def test_app_icon_keeps_a_margin_from_the_edge(qapp):
    from dk_tracker.ui.icons import app_icon

    image = app_icon().pixmap(64, 64).toImage()
    for x in range(64):
        assert QColor.fromRgba(image.pixel(x, 0)).alpha() == 0
        assert QColor.fromRgba(image.pixel(0, x)).alpha() == 0


def test_theme_assets_that_cannot_be_written_are_skipped(tmp_path):
    from dk_tracker.ui.theme import write_assets

    blocker = tmp_path / "not-a-directory"
    blocker.write_text("")
    assert write_assets(DARK, blocker / "theme") == {}
    assert "QComboBox::down-arrow" not in stylesheet(DARK, {})


def test_asset_paths_with_spaces_are_quoted(tmp_path):
    from dk_tracker.ui.theme import write_assets

    assets = write_assets(DARK, tmp_path / "Kimai App" / "theme")
    assert f'url("{assets["chevron"]}")' in stylesheet(DARK, assets)


def test_header_mark_is_readable_on_the_window_background(qapp):
    """0065: the 18 px dark tile vanished on the dark header; the mark has no tile and themed letters."""
    from dk_tracker.ui.icons import mark

    image = mark("#ffffff", 24).toImage()
    assert image.width() >= 24
    assert QColor.fromRgba(image.pixel(0, 0)).alpha() == 0  # no tile: the corners stay clear
    letters = [QColor.fromRgba(image.pixel(x, image.height() // 2)) for x in range(image.width())]
    assert any(c.alpha() > 200 and min(c.red(), c.green(), c.blue()) > 200 for c in letters)  # white letters


def test_window_header_shows_the_mark_at_24_px(qapp):
    from dk_tracker.core.i18n import Translator
    from dk_tracker.core.settings import Settings
    from dk_tracker.ui.popup import QuickWindow
    from dk_tracker.ui.state import AppState

    popup = QuickWindow(AppState(Settings(), Translator("pl")))
    assert popup.logo.pixmap().deviceIndependentSize().width() == 24
