# DIM

**Status:** Supported  
**Category:** Arrays

Allocate zero-based arrays with inclusive upper bounds.

## Syntax

```basic
DIM name(upper [, upper ...]) [, name(upper ...) ...]
```

## Parameters

- name: array variable, optionally with a type suffix.
- upper: nonnegative upper index, not the element count. DIM A(4) has five cells.

## Use cases

- Store marks for several students.
- Store rows and columns of a small grid.

## Examples

### Example 1 (program)

```basic
10 DIM A(2)
20 A(0)=10: A(2)=30
30 PRINT A(0)+A(2)
```

Expected output / effect:

```text
 40 
```

## Notes

- Indices are zero-based. Implicit arrays default to upper bound 10 in each dimension.
- Cumulative array capacity is 100,000 cells. Duplicate DIM, bad rank and out-of-range subscripts raise errors.
- OPTION BASE, REDIM, AS declarations and user-defined array types are not implemented.

[Back to keyword index](INDEX.md)
