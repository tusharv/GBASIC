10 REM 07 - Number triangle: use the column number instead of a star.
20 REM MID$(STR$(COL),2) removes the leading space from positive numbers.
30 REM Use N from 1 to 9 so each column remains one digit wide.
40 N=5
50 FOR ROW=1 TO N
60 FOR COL=1 TO ROW
70 PRINT MID$(STR$(COL),2);
80 NEXT COL
90 PRINT
100 NEXT ROW
110 REM Try: print ROW instead of COL. Predict each line.
120 END
