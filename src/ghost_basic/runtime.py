"""Bounded, inspectable execution machine with explicit control-flow stacks."""

import csv
import math
import sys
from dataclasses import dataclass

from .devices import TextInput, TextOutput
from .errors import BasicError
from .evaluator import evaluate
from .parser import Parser
from .program import Program
from .syntax import Expr, Reference, Statement
from .values import Kind, Value, coerce, default, formatted, numeric


@dataclass
class Instruction:
    line: int
    statement: Statement
    destination: int = -1


@dataclass
class Loop:
    name: str
    end: float
    step: float
    body: int


@dataclass
class Array:
    dimensions: tuple[int, ...]
    cells: dict[tuple[int, ...], Value]


class Runtime:
    def __init__(
        self,
        *,
        output: TextOutput | None = None,
        input_stream: TextInput | None = None,
        max_steps: int = 100_000,
        max_cells: int = 100_000,
    ) -> None:
        self.output: TextOutput = output if output is not None else sys.stdout
        self.input: TextInput = input_stream if input_stream is not None else sys.stdin
        self.max_steps = max_steps
        self.max_cells = max_cells
        self.variables: dict[str, Value] = {}
        self.arrays: dict[str, Array] = {}
        self.instructions: list[Instruction] = []
        self.line_map: dict[int, int] = {}
        self.returns: list[int] = []
        self.loops: list[Loop] = []
        self.data: list[tuple[int, Value]] = []
        self.data_pointer = 0
        self.pc = 0
        self.steps = 0
        self.column = 0
        self.halted = True

    def value(self, expr: Expr) -> Value:
        return evaluate(expr, self.lookup)

    def lookup(self, ref: Reference) -> Value:
        if ref.indices:
            array, key = self.cell(ref)
            return array.cells.get(key, default(ref.name))
        return self.variables.get(ref.name, default(ref.name))

    def cell(self, ref: Reference) -> tuple[Array, tuple[int, ...]]:
        if ref.name not in self.arrays:
            self.dimension(ref.name, tuple(10 for _ in ref.indices))
        array = self.arrays[ref.name]
        key = tuple(self.value(e).integer() for e in ref.indices)
        if len(key) != len(array.dimensions) or any(
            k < 0 or k > upper for k, upper in zip(key, array.dimensions)
        ):
            raise BasicError("Subscript out of range")
        return array, key

    def assign(self, ref: Reference, value: Value) -> None:
        value = coerce(ref.name, value)
        if ref.indices:
            array, key = self.cell(ref)
            array.cells[key] = value
        else:
            self.variables[ref.name] = value

    def dimension(self, name: str, dimensions: tuple[int, ...]) -> None:
        if name in self.arrays:
            raise BasicError("Duplicate definition")
        if not dimensions or any(n < 0 for n in dimensions):
            raise BasicError("Illegal function call")
        total = sum(math.prod(n + 1 for n in a.dimensions) for a in self.arrays.values())
        if total + math.prod(n + 1 for n in dimensions) > self.max_cells:
            raise BasicError("Out of memory")
        self.arrays[name] = Array(dimensions, {})

    def emit(self, text: str) -> None:
        self.output.write(text)
        self.column = len(text.rsplit("\n", 1)[1]) if "\n" in text else self.column + len(text)

    def prepare(self, program: Program, *, reset: bool = True) -> None:
        if reset:
            self.variables.clear()
            self.arrays.clear()
        self.instructions.clear()
        self.line_map.clear()
        self.returns.clear()
        self.loops.clear()
        self.data.clear()
        self.data_pointer = self.pc = self.steps = 0
        self.halted = True
        for line, source in sorted(program.lines.items()):
            self.line_map[line] = len(self.instructions)
            try:
                self.compile(line, Parser(source).parse())
            except (BasicError, RecursionError) as error:
                if isinstance(error, RecursionError):
                    raise BasicError("Expression too complex", line) from None
                error.line = line
                raise
        self.halted = False

    def compile(self, line: int, statements: tuple[Statement, ...]) -> None:
        for statement in statements:
            if statement.op == "IF":
                conditional = Instruction(line, Statement("BRANCH", statement.expressions))
                self.instructions.append(conditional)
                self.compile(line, statement.then_body)
                jump = Instruction(line, Statement("JUMP"))
                self.instructions.append(jump)
                conditional.destination = len(self.instructions)
                self.compile(line, statement.else_body)
                jump.destination = len(self.instructions)
            elif statement.op == "NEXT" and len(statement.targets) > 1:
                for target in statement.targets:
                    self.instructions.append(
                        Instruction(line, Statement("NEXT", targets=(target,)))
                    )
            else:
                self.instructions.append(Instruction(line, statement))
                if statement.op == "DATA":
                    self.data.extend((line, self.value(expr)) for expr in statement.expressions)

    def run(self, program: Program, *, reset: bool = True) -> None:
        self.prepare(program, reset=reset)
        while not self.halted:
            self.step()

    def step(self) -> bool:
        """Execute one instruction. Callers can inspect pc and variables between steps."""
        if self.halted or self.pc >= len(self.instructions):
            self.halted = True
            return False
        instruction = self.instructions[self.pc]
        if self.steps >= self.max_steps:
            self.halted = True
            raise BasicError("Execution limit exceeded", instruction.line)
        self.steps += 1
        self.pc += 1
        try:
            self.execute(instruction)
        except BasicError as error:
            self.halted = True
            error.line = instruction.line
            raise
        return True

    def jump(self, expression: Expr) -> None:
        n = self.value(expression).number()
        if not n.is_integer() or int(n) not in self.line_map:
            raise BasicError("Undefined line number")
        self.pc = self.line_map[int(n)]

    def matching(self, start: str, end: str) -> int:
        depth = 1
        for index in range(self.pc, len(self.instructions)):
            op = self.instructions[index].statement.op
            if op == start:
                depth += 1
            elif op == end:
                depth -= 1
                if depth == 0:
                    return index
        raise BasicError(f"{start} without {end}")

    def execute(self, instruction: Instruction) -> None:
        stmt = instruction.statement
        op = stmt.op
        if op == "LET":
            self.assign(stmt.targets[0], self.value(stmt.expressions[0]))
        elif op == "PRINT":
            for expr, separator in zip(stmt.expressions, stmt.separators):
                self.emit(formatted(self.value(expr)))
                if separator == ",":
                    self.emit(" " * (14 - self.column % 14))
            if not stmt.separators or stmt.separators[-1] == "":
                self.emit("\n")
        elif op == "BRANCH":
            if not self.value(stmt.expressions[0]).number():
                self.pc = instruction.destination
        elif op == "JUMP":
            self.pc = instruction.destination
        elif op in ("END", "STOP"):
            self.halted = True
        elif op in ("GOTO", "GOSUB"):
            if op == "GOSUB":
                self.returns.append(self.pc)
            self.jump(stmt.expressions[0])
        elif op == "RETURN":
            if not self.returns:
                raise BasicError("RETURN without GOSUB")
            self.pc = self.returns.pop()
        elif op == "FOR":
            end_index = self.matching("FOR", "NEXT")
            start, end, step = [self.value(e).number() for e in stmt.expressions]
            if step == 0:
                raise BasicError("Illegal function call: zero STEP")
            self.assign(stmt.targets[0], numeric(start))
            if start > end if step > 0 else start < end:
                self.pc = end_index + 1
            else:
                name = stmt.targets[0].name
                # Re-entering FOR with an active variable replaces that loop and inner loops.
                found = next((i for i, loop in enumerate(self.loops) if loop.name == name), None)
                if found is not None:
                    del self.loops[found:]
                self.loops.append(Loop(name, end, step, self.pc))
        elif op == "NEXT":
            if not self.loops:
                raise BasicError("NEXT without FOR")
            loop = self.loops[-1]
            if stmt.targets and stmt.targets[0].name != loop.name:
                raise BasicError("NEXT without FOR")
            ref = Reference(loop.name)
            self.assign(ref, numeric(self.lookup(ref).number() + loop.step))
            n = self.lookup(ref).number()
            if n <= loop.end if loop.step > 0 else n >= loop.end:
                self.pc = loop.body
            else:
                self.loops.pop()
        elif op == "WHILE":
            end_index = self.matching("WHILE", "WEND")
            if not self.value(stmt.expressions[0]).number():
                self.pc = end_index + 1
        elif op == "WEND":
            depth = 1
            for index in range(self.pc - 2, -1, -1):
                other = self.instructions[index].statement.op
                if other == "WEND":
                    depth += 1
                elif other == "WHILE":
                    depth -= 1
                    if depth == 0:
                        self.pc = index
                        break
            else:
                raise BasicError("WEND without WHILE")
        elif op == "DIM":
            for ref in stmt.targets:
                self.dimension(ref.name, tuple(self.value(e).integer() for e in ref.indices))
        elif op == "READ":
            for ref in stmt.targets:
                if self.data_pointer >= len(self.data):
                    raise BasicError("Out of DATA")
                self.assign(ref, self.data[self.data_pointer][1])
                self.data_pointer += 1
        elif op == "RESTORE":
            line = self.value(stmt.expressions[0]).number() if stmt.expressions else 0
            if stmt.expressions and line not in self.line_map:
                raise BasicError("Undefined line number")
            self.data_pointer = next(
                (i for i, (n, _) in enumerate(self.data) if n >= line), len(self.data)
            )
        elif op == "INPUT":
            self.emit(stmt.text + "? ")
            raw = self.input.readline()
            if not raw:
                raise BasicError("Input past end")
            try:
                fields = next(csv.reader([raw.rstrip("\r\n")], skipinitialspace=True))
                if len(fields) != len(stmt.targets):
                    raise ValueError
                values = [
                    Value(Kind.STRING, text) if ref.name.endswith("$") else numeric(float(text))
                    for ref, text in zip(stmt.targets, fields)
                ]
            except (ValueError, csv.Error):
                raise BasicError("Redo from start") from None
            for ref, value in zip(stmt.targets, values):
                self.assign(ref, value)
        elif op == "CLS":
            self.emit("\x1b[2J\x1b[H")
        elif op == "BEEP":
            self.emit("\a")
        elif op != "DATA":
            raise BasicError(f"Unsupported statement: {op}")
