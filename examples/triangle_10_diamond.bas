10 REM 10 - Diamond: join an upright and an inverted pyramid.
20 REM The second half starts at N-1 so the widest row is not repeated.
30 N=5
40 FOR ROW=1 TO N
50 GOSUB 300
60 NEXT ROW
70 FOR ROW=N-1 TO 1 STEP -1
80 GOSUB 300
90 NEXT ROW
100 REM Try: start the second half at N. Which row is repeated?
110 END
300 FOR COL=1 TO N-ROW
310 PRINT " ";
320 NEXT COL
330 FOR COL=1 TO 2*ROW-1
340 PRINT "*";
350 NEXT COL
360 PRINT
370 RETURN
