"""Cancellable BASIC execution, with bounded queues and no UI dependencies."""

import queue
import threading
from dataclasses import dataclass

from .errors import BasicError
from .program import Program
from .runtime import Runtime


class _Cancelled(Exception):
    pass


@dataclass(frozen=True)
class ExecutionEvent:
    kind: str
    text: str = ""


class _Output:
    def __init__(self, runner: "ProgramRunner") -> None:
        self.runner = runner
        self.count = 0

    def write(self, text: str) -> int:
        self.count += len(text)
        if self.count > self.runner.max_output:
            raise BasicError("Output limit exceeded")
        self.runner.publish("output", text)
        return len(text)


class _Input:
    def __init__(self, runner: "ProgramRunner") -> None:
        self.runner = runner

    def readline(self, size: int | None = -1) -> str:
        self.runner.publish("input")
        while not self.runner.cancelled.is_set():
            try:
                return self.runner.inputs.get(timeout=0.05) + "\n"
            except queue.Empty:
                continue
        raise _Cancelled


class ProgramRunner:
    """One owned worker; all widget updates are performed by the UI's event poller."""

    def __init__(self, *, max_steps: int = 100_000, max_output: int = 200_000) -> None:
        self.max_steps = max_steps
        self.max_output = max_output
        self.events: queue.Queue[ExecutionEvent] = queue.Queue(maxsize=256)
        self.inputs: queue.Queue[str] = queue.Queue(maxsize=1)
        self.cancelled = threading.Event()
        self.thread: threading.Thread | None = None
        self.runtime: Runtime | None = None

    @property
    def running(self) -> bool:
        return self.thread is not None and self.thread.is_alive()

    def publish(self, kind: str, text: str = "") -> None:
        while not self.cancelled.is_set():
            try:
                self.events.put(ExecutionEvent(kind, text), timeout=0.05)
                return
            except queue.Full:
                continue
        raise _Cancelled

    def start(self, source: str, *, immediate: bool = False) -> None:
        if self.running:
            raise BasicError("Program is already running")
        self.drain()
        self.cancelled.clear()
        self.inputs = queue.Queue(maxsize=1)
        self.thread = threading.Thread(target=self._execute, args=(source, immediate), daemon=True)
        self.thread.start()

    def _execute(self, source: str, immediate: bool) -> None:
        output = _Output(self)
        input_stream = _Input(self)
        if self.runtime is None:
            self.runtime = Runtime(max_steps=self.max_steps)
        self.runtime.output = output
        self.runtime.input = input_stream
        try:
            program = Program({0: source}) if immediate else Program.from_source(source)
            self.runtime.prepare(program, reset=not immediate)
            while not self.runtime.halted:
                if self.cancelled.is_set():
                    raise _Cancelled
                self.runtime.step()
        except _Cancelled:
            pass
        except BasicError as error:
            self._finish_event("error", str(error))
        finally:
            if self.cancelled.is_set():
                self._finish_event("stopped", "Stopped")
            self._finish_event("done")

    def _finish_event(self, kind: str, text: str = "") -> None:
        # Even cancellation must report completion; make room if the UI is closing.
        event = ExecutionEvent(kind, text)
        while True:
            try:
                self.events.put(event, timeout=0.05)
                return
            except queue.Full:
                if self.cancelled.is_set():
                    try:
                        self.events.get_nowait()
                    except queue.Empty:
                        pass

    def drain(self) -> list[ExecutionEvent]:
        events = []
        for _ in range(256):
            try:
                events.append(self.events.get_nowait())
            except queue.Empty:
                break
        return events

    def send_input(self, text: str) -> None:
        try:
            self.inputs.put_nowait(text[:32767])
        except queue.Full:
            raise BasicError("Input is already pending") from None

    def stop(self) -> None:
        self.cancelled.set()

    def join(self, timeout: float = 0.2) -> None:
        if self.thread:
            self.thread.join(timeout)
