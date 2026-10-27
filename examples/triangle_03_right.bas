10 REM 03 - Right-aligned triangle: spaces first, then stars.
20 REM Every row has N-ROW spaces and ROW stars: total width N.
30 N=5
40 FOR ROW=1 TO N
50 FOR COL=1 TO N-ROW
60 PRINT " ";
70 NEXT COL
80 FOR COL=1 TO ROW
90 PRINT "*";
100 NEXT COL
110 PRINT
120 NEXT ROW
130 REM Try: print dots instead of spaces to see the padding.
140 END
