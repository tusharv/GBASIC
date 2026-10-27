10 REM 01 - Left triangle: outer loop chooses the row.
20 REM The inner loop prints ROW stars. Semicolon keeps the same line.
30 N=5
40 FOR ROW=1 TO N
50 FOR COL=1 TO ROW
60 PRINT "*";
70 NEXT COL
80 PRINT
90 NEXT ROW
100 REM Try: change N to 3, then predict the output before Run.
110 END
