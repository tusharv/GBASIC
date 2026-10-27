10 REM 09 - Pascal triangle: each row starts and ends with 1.
20 REM For row R, next coefficient = current * (R-COL) / COL.
30 REM Small values divide exactly. Integer division uses a backslash.
40 REM Use N from 1 to 5 for this single-digit aligned exercise.
50 N=5
60 FOR ROW=1 TO N
70 FOR PAD=1 TO N-ROW
80 PRINT " ";
90 NEXT PAD
100 COEFF=1
110 FOR COL=1 TO ROW
120 PRINT MID$(STR$(COEFF),2);" ";
130 IF COL<ROW THEN COEFF=COEFF*(ROW-COL)\COL
140 NEXT COL
150 PRINT
160 NEXT ROW
170 REM Try: add up the coefficients in each row: 1,2,4,8,16.
180 END
