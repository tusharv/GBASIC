# INPUT

**Status:** Supported  
**Category:** Input/output

Read one line of user input into one or more numeric or string variables.

## Syntax

```basic
INPUT ["prompt";] variable [, variable ...]
```

## Parameters

- prompt: optional quoted text followed by a semicolon; ? is appended.
- variable: a scalar or array element; use a $ suffix for strings.
- Multiple targets require comma-separated fields in one answer.

## Use cases

- Ask for principal, rate and time.
- Collect a name and an age.

## Examples

### Example 1 (program)

```basic
10 INPUT "Name";N$
20 INPUT "Age";A%
30 PRINT N$;A%
```

Input (one answer per line):

```text
Ada
30
```

Expected output / effect:

```text
Name? Age? Ada 30 
```

## Notes

- Malformed input raises Redo from start and ends the run; automatic retry is not implemented.
- Numeric fields must be plain numbers, without percent/currency symbols. In the UI use the bottom INPUT field.

[Back to keyword index](INDEX.md)
