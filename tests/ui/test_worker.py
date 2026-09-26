import threading

from dk_tracker.ui.worker import Worker


def test_job_runs_in_the_background_and_answers_on_the_gui_thread(qtbot):
    worker = Worker("test")
    gui = threading.get_ident()
    seen = {}

    def job():
        seen["job"] = threading.get_ident()
        return 42

    def done(value):
        seen["done"] = (threading.get_ident(), value)

    worker.submit(job, done)
    qtbot.waitUntil(lambda: "done" in seen)
    assert seen["job"] != gui
    assert seen["done"] == (gui, 42)
    worker.shutdown()


def test_jobs_run_one_at_a_time_in_order(qtbot):
    worker = Worker("test")
    order = []
    for number in range(5):
        worker.submit(lambda number=number: order.append(number))
    qtbot.waitUntil(lambda: len(order) == 5)
    assert order == [0, 1, 2, 3, 4]
    worker.shutdown()


def test_errors_reach_the_error_callback(qtbot):
    worker = Worker("test")
    caught = []

    def boom():
        raise ValueError("nope")

    worker.submit(boom, on_error=caught.append)
    qtbot.waitUntil(lambda: bool(caught))
    assert isinstance(caught[0], ValueError)
    worker.shutdown()


def test_a_keyed_job_is_not_queued_twice(qtbot):
    worker = Worker("test")
    gate = threading.Event()
    runs = []
    worker.submit(gate.wait)  # keeps the thread busy
    assert worker.submit(lambda: runs.append(1), key="refresh") is True
    assert worker.submit(lambda: runs.append(2), key="refresh") is False
    gate.set()
    qtbot.waitUntil(lambda: runs == [1])
    qtbot.wait(50)
    assert runs == [1]
    assert worker.submit(lambda: runs.append(3), key="refresh") is True  # free again once done
    qtbot.waitUntil(lambda: runs == [1, 3])
    worker.shutdown()


def test_nothing_is_accepted_after_shutdown(qtbot):
    worker = Worker("test")
    worker.shutdown()
    assert worker.submit(lambda: None) is False


def test_busy_until_every_answer_arrived(qtbot):
    worker = Worker("test")
    gate = threading.Event()
    worker.submit(gate.wait)
    assert worker.busy
    gate.set()
    qtbot.waitUntil(lambda: not worker.busy)
    worker.shutdown()


def test_finish_runs_what_is_queued_and_then_refuses_new_jobs(qtbot):
    worker = Worker("test")
    done = []
    gate = threading.Event()
    worker.submit(gate.wait)
    worker.submit(lambda: done.append("queued"))
    gate.set()
    assert worker.finish(timeout=2.0) is True
    assert done == ["queued"]
    assert worker.submit(lambda: None) is False
