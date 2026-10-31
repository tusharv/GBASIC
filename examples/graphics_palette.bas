10 REM Sixteen fixed colors in a four-by-four grid. Change C to explore.
20 SCREEN 7
30 FOR C=0 TO 15
40 X=(C MOD 4)*80
50 Y=(C\4)*50
60 LINE (X+2,Y+2)-(X+77,Y+47),C,BF
70 NEXT C
80 PRINT "Palette ready. Press F9 to view."
90 END
