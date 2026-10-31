# Expression precision and numeric examples

Execute inline under the existing autonomous implementation instruction.
Spec: ROADMAP.md numeric continuation; user additionally requests examples.
Reference: GW-BASIC User's Guide chapter 6, type conversion and arithmetic.

Design: use the widest operand kind for +, -, * and /; integer division using /
produces single. Integer +, -, * overflow promotes to single. Round every single
result before it is used by the next expression. ABS/INT/FIX preserve argument kind,
with ABS(-32768) promoted to single. Keep existing exponentiation, transcendental
functions, VAL, Unicode strings and IEEE-vs-MBF limitations explicitly documented.

- [x] Write failing tests for result kinds, rounding between operations, mixed operands,
  overflow, division errors, intrinsic precision, and exact example output.
- [x] Implement shared numeric-result promotion and evaluator integration.
- [x] Add three numbered numeric_*.bas examples, expected-output tests, source packaging,
  learning guide, differential probe and compatibility updates.
- [x] Full test/lint/format/type/build verification and independent read-only review.

Review focus: integer overflow must promote without wrapping; double operands must not
round to single; assignment to double must not recover precision already lost; existing
string operations and error handling must remain intact; examples must ship in the sdist.

Verification: 505 passed, 1 skipped; lint/format/types and builds passed.
Independent review found no substantive issues. Source archive includes all three examples.
