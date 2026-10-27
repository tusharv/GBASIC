10 REM 04 - Centered pyramid: odd widths are 1,3,5,7,9.
20 REM Row R uses N-R leading spaces and 2*R-1 stars.
30 N=5
40 FOR ROW=1 TO N
50 FOR COL=1 TO N-ROW
60 PRINT " ";
70 NEXT COL
80 FOR COL=1 TO 2*ROW-1
90 PRINT "*";
100 NEXT COL
110 PRINT
120 NEXT ROW
130 REM Try: use 2*ROW stars. What changes?
140 END
