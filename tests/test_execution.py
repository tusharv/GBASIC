import time

from ghost_basic.execution import ProgramRunner


def collect_until(runner, kind, timeout=3):
    events = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        events.extend(runner.drain())
        if any(event.kind == kind for event in events):
            return events
        time.sleep(0.01)
    raise AssertionError(f"Timed out waiting for {kind}: {events}")


def test_runner_output_and_errors():
    runner = ProgramRunner()
    runner.start('10 PRINT "Hello";1\n20 PRINT 1/0')
    events = collect_until(runner, "done")
    assert "".join(e.text for e in events if e.kind == "output") == "Hello 1 \n"
    assert any(e.kind == "error" and "Division by zero in 20" in e.text for e in events)


def test_runner_interactive_input():
    runner = ProgramRunner()
    runner.start('10 INPUT "Name";N$\n20 PRINT "Hi ";N$')
    initial = collect_until(runner, "input")
    assert "".join(e.text for e in initial if e.kind == "output") == "Name? "
    runner.send_input("Ada")
    rest = collect_until(runner, "done")
    assert "".join(e.text for e in rest if e.kind == "output") == "Hi Ada\n"


def test_stop_input_wait():
    runner = ProgramRunner()
    runner.start("10 INPUT N$")
    collect_until(runner, "input")
    runner.stop()
    events = collect_until(runner, "done")
    assert any(e.kind == "stopped" for e in events)
    runner.join(1)
    assert not runner.running


def test_stop_loop_and_restart():
    runner = ProgramRunner(max_steps=100_000_000)
    runner.start("10 GOTO 10")
    runner.stop()
    collect_until(runner, "done")
    runner.join(1)
    assert not runner.running
    runner.start('10 PRINT "again"')
    events = collect_until(runner, "done")
    assert any("again" in e.text for e in events)


def test_output_budget():
    runner = ProgramRunner(max_output=100)
    runner.start('10 PRINT STRING$(1000,"a")')
    events = collect_until(runner, "done")
    assert any(e.kind == "error" and "Output limit" in e.text for e in events)
