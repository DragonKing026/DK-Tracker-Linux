"""UI tests run without a display: Qt's offscreen platform, set before QApplication exists.
Theme files go to a throwaway cache, not the user's ~/.cache."""

import os
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["XDG_CACHE_HOME"] = tempfile.mkdtemp(prefix="ws-tracker-tests-")
