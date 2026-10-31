10 REM Nested loops build alternating tiles. F5 run, F9 preview.
20 REM Change the two tile colors 15 and 9, or the margin X=60.
30 SCREEN 7
40 COLOR 15,8: CLS
50 FOR ROW=0 TO 7
60 FOR COL=0 TO 7
70 C=15
80 IF (ROW+COL) MOD 2=1 THEN C=9
90 X=60+COL*25: Y=ROW*25
100 LINE (X,Y)-(X+24,Y+24),C,BF
110 NEXT COL
120 NEXT ROW
130 PRINT "Checkerboard ready. Press F9 to view."
140 END
