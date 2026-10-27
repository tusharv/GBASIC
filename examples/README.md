# Logic-building exercises

Open Ghost BASIC, press **F3**, and choose a program from the examples dropdown.
Press Enter to select, Enter again to open, and **F5** to run. If the editor has unsaved
work, save with F2 first. Read the numbered REM comments: they explain the logic and
suggest a change to try. No additional installation or unsupported QBasic features needed.

## A good practice routine

1. Draw the expected output on paper before pressing F5.
2. Find the row loop and each column loop. Trace ROW, COL and any accumulator by hand.
3. Change `N=5` to `N=3` in the editor; predict how every line changes.
4. Run and compare. Try `N=1` to find off-by-one errors.
5. Complete the challenge in the program's REM comments. Use F4 to save your own variant.

`FOR ROW=1 TO N` controls the number of lines. An inner FOR controls characters on that
line. `PRINT "*";` stays on the current line; a bare `PRINT` finishes it. `NEXT` returns to
the matching loop. A start larger than the end skips a positive-step loop, which is useful
when a row needs zero spaces. In `STEP -1` loops, the direction is reversed.

## Pattern learning path

All pattern programs start at five rows. Work through them in order:

| File | Pattern | Main idea / challenge |
| --- | --- | --- |
| triangle_01_left.bas | Left-aligned triangle | Print ROW stars; vary the height |
| triangle_02_inverted.bas | Inverted left triangle | Count backward with STEP -1; try STEP -2 |
| triangle_03_right.bas | Right-aligned triangle | N-ROW spaces, then ROW stars; replace spaces with dots |
| triangle_04_pyramid.bas | Centered pyramid | Odd widths: 2*ROW-1 stars; try an even width |
| triangle_05_inverted_pyramid.bas | Inverted pyramid | Reverse the row order; predict the last row's padding |
| triangle_06_hollow.bas | Hollow triangle | Use IF/OR to select the edges and base |
| triangle_07_numbers.bas | 1 / 12 / 123 | Print COL; then try printing ROW |
| triangle_08_floyd.bas | 1 / 2 3 / 4 5 6 | Keep a counter across rows; try resetting it per row |
| triangle_09_pascal.bas | 1 / 1 1 / 1 2 1 | Calculate each coefficient; find each row's sum |
| triangle_10_diamond.bas | Two joined pyramids | Reuse a drawing subroutine; avoid repeating the middle row |

### Left triangle

```text
*
**
***
****
*****
```

### Centered pyramid

```text
    *
   ***
  *****
 *******
*********
```

### Hollow triangle

```text
*
**
* *
*  *
*****
```

### Floyd's triangle

```text
1
2 3
4 5 6
7 8 9 10
11 12 13 14 15
```

### Pascal's triangle

```text
    1
   1 1
  1 2 1
 1 3 3 1
1 4 6 4 1
```

Pascal's coefficients use `COEFF*(ROW-COL)\COL`. The backslash is integer division;
for these small coefficients every division is exact. Keep N between 1 and 5 for this
single-digit centered layout. Larger rows need wider number fields. The numbered-triangle
exercise similarly assumes single-digit columns (N <= 9). Floyd and Pascal print a trailing
space after each value; the tests preserve these spaces even though the diagrams omit them.
`MID$(STR$(number),2)` removes BASIC's leading space before positive numbers so digits align.

## Other logic exercises

| File | Starting values and result | What to practice |
| --- | --- | --- |
| logic_sum.bas | N=10 gives 55 | Accumulator starts at zero; try odd numbers with STEP 2 |
| logic_factorial.bas | N=5 gives 120 | Product starts at one; try N=0 (answer 1) |
| logic_prime.bas | N=29 prints Prime | MOD tests divisibility; a flag remembers a divisor |

Use small nonnegative whole numbers for the prime exercise; try 1, 2 and 9. Trial division
only needs to reach INT(SQR(N)), since a composite number has a factor no larger than its
square root. The factorial exercise is intended for N from 0 to 10. These are small learning
programs, not arbitrary-precision numerical tools; the interpreter's numeric limits apply.

Once comfortable, combine the ideas: draw a hollow pyramid, print only even numbers in a
triangle, calculate the sum of each row, or join two right triangles into an hourglass.

The original hello, fibonacci, subroutines, data, input, while and types samples remain
available alongside these exercises. The learning gallery now has 42 programs with automated output checks, including the
[22 input-based calculators](CALCULATORS.md): simple/compound interest and 20 everyday exercises.
