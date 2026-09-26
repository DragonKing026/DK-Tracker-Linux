"""Background jobs for the UI: HTTP to Kimai and D-Bus calls never run on the GUI thread.

Each Worker owns one thread, so its jobs run one at a time in submission order — the tracker
and a D-Bus connection are not thread-safe, and actions reach Kimai in the order they were
clicked (spec, section 5). Results come back on the GUI thread through a queued signal.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any

from PySide6.QtCore import QObject, Signal

log = logging.getLogger(__name__)


class Worker(QObject):
    _finished = Signal(object)  # a callable to run on the GUI thread

    def __init__(self, name: str, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix=f"ws-tracker-tray-{name}")
        self._pending: set[str] = set()
        self._inflight = 0  # submitted and not yet answered
        self._closed = False
        # Emitted from the worker thread; the receiver lives on the GUI thread, so Qt queues it.
        self._finished.connect(self._deliver)

    def submit(
        self,
        job: Callable[[], Any],
        on_done: Callable[[Any], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        *,
        key: str | None = None,
    ) -> bool:
        """Queue a job; with a key, a second one is dropped while the first still waits or runs."""
        if self._closed or (key is not None and key in self._pending):
            return False
        if key is not None:
            self._pending.add(key)
        self._inflight += 1

        def run() -> None:
            try:
                result = job()
            except Exception as error:  # noqa: BLE001 - handed to the caller on the GUI thread
                outcome = partial(self._complete, key, on_error, error, failed=True)
            else:
                outcome = partial(self._complete, key, on_done, result, failed=False)
            self._finished.emit(outcome)

        self._executor.submit(run)
        return True

    @property
    def busy(self) -> bool:
        return self._inflight > 0

    def finish(self, timeout: float) -> bool:
        """Accept nothing new, run what is queued (answers are no longer delivered); False on timeout."""
        if self._closed:
            return True
        self._closed = True
        finished = threading.Event()
        self._executor.submit(finished.set)  # runs after every job queued before it
        self._executor.shutdown(wait=False)
        return finished.wait(timeout)

    def shutdown(self, wait: bool = False) -> None:
        self._closed = True
        self._executor.shutdown(wait=wait, cancel_futures=True)

    def _complete(
        self, key: str | None, callback: Callable[[Any], None] | None, value: Any, *, failed: bool
    ) -> None:
        self._inflight -= 1
        if key is not None:
            self._pending.discard(key)
        if callback is not None:
            callback(value)
        elif failed:
            log.error("Background job failed", exc_info=value)

    @staticmethod
    def _deliver(outcome: Callable[[], None]) -> None:
        outcome()
