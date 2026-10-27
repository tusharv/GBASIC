# DATA

**Status:** Supported  
**Category:** Data

Store literal values in the program for READ statements.

## Syntax

```basic
DATA literal [, literal ...]
```

## Parameters

- items: numeric literals (optionally signed) or quoted strings separated by commas.

## Use cases

- Load a fixed list of scores.
- Replay a small table without keyboard input.

## Examples

### Example 1 (program)

```basic
10 DATA 5,6,"Ada"
20 READ A,B,N$
30 PRINT A+B;N$
40 RESTORE
50 READ X
60 PRINT X
```

Expected output / effect:

```text
 11 Ada
 5 
```

## Notes

- Unquoted DATA strings and calculated DATA expressions are not supported. READ past the end raises Out of DATA.
- DATA is collected before execution, even if the DATA line is skipped by control flow.

[Back to keyword index](INDEX.md)
