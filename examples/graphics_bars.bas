10 REM DATA values become bar heights. F5 run, F9 preview.
20 REM Try new heights from 1 to 150 in line 40.
30 SCREEN 7
40 DATA 40,90,65,135,110
50 FOR I=0 TO 4
60 READ H
70 X=40+I*50
80 LINE (X,180-H)-(X+29,179),I+9,BF
90 NEXT I
100 LINE (25,20)-(25,180),15
110 LINE (25,180)-(300,180),15
120 FOR Y=30 TO 180 STEP 30
130 LINE (21,Y)-(25,Y),7
140 NEXT Y
150 PRINT "Bar chart ready. Press F9 to view."
160 END
