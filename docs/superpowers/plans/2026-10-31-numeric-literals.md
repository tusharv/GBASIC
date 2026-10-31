# Numeric literal fidelity

Execute inline under the existing autonomous implementation instruction.
Goal: classify integer/single/double literals and interpret GW-BASIC radix literals
as signed 16-bit values, including the short octal prefix. Keep IEEE representation.
References: GW-BASIC User's Guide chapter 6, sections 6.1 and 6.1.1, and appendix G.

Approach: centralize literal conversion in values.py; parser delegates after lexing.
Suffixes override default precision. E selects single, D selects double; otherwise
seven or fewer significant decimal digits select single, eight or more select double.
Plain whole numbers in 0..32767 select integer. Radix values are bounded to 0..65535
and interpreted in two's complement. Unary signs preserve floating precision; integer
negation outside signed 16-bit range promotes to single. Existing binary arithmetic
promotion, VAL parsing, MBF representation and codepage semantics are out of scope.

- [x] Add failing classification, signed-radix, overflow, unary and runtime DATA tests.
- [x] Implement conversion and short-octal lexing; preserve BASIC errors for huge inputs.
- [x] Extend manual-linked comparison cases and update compatibility/help if needed.
- [x] Verify full tests, lint, format, types and build; independent final review.

Review focus: leading zeros, suffix/exponent precedence, oversized values, unary minus
at the signed boundary, and preservation of DATA/line-number parsing.

Verification: 469 passed, 1 skipped; focused 39 passed after local-name typing fix.
Lint/format/strict types passed; independent review found no substantive issues.
