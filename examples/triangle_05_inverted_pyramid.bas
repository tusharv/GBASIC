10 REM 05 - Inverted pyramid: reverse the row order of example 04.
20 N=5
30 FOR ROW=N TO 1 STEP -1
40 FOR COL=1 TO N-ROW
50 PRINT " ";
60 NEXT COL
70 FOR COL=1 TO 2*ROW-1
80 PRINT "*";
90 NEXT COL
100 PRINT
110 NEXT ROW
120 REM Try: predict the number of spaces on the last row.
130 END
