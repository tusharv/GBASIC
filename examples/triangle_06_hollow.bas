10 REM 06 - Hollow triangle: print stars only on the boundary.
20 REM Boundaries: first column, diagonal COL=ROW, or last row.
30 N=5
40 FOR ROW=1 TO N
50 FOR COL=1 TO ROW
60 IF COL=1 OR COL=ROW OR ROW=N THEN PRINT "*"; ELSE PRINT " ";
70 NEXT COL
80 PRINT
90 NEXT ROW
100 REM Try: remove ROW=N from the condition. What happens to the base?
110 END
