"""UI tests run without a display: Qt's offscreen platform, set before QApplication exists."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
