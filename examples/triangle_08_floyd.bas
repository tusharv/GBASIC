10 REM 08 - Floyd triangle: one counter continues across all rows.
20 N=5
30 NUMBER=1
40 FOR ROW=1 TO N
50 FOR COL=1 TO ROW
60 PRINT MID$(STR$(NUMBER),2);" ";
70 NUMBER=NUMBER+1
80 NEXT COL
90 PRINT
100 NEXT ROW
110 REM Try: move NUMBER=1 inside the row loop. How does it differ?
120 END
