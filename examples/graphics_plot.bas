10 REM Plot a sine wave using PSET. Try changing the amplitude 60.
20 SCREEN 7
30 LINE (0,100)-(319,100),8
40 LINE (160,0)-(160,199),8
50 FOR X=0 TO 319
60 Y=100-60*SIN(X/25)
70 PSET (X,Y),14
80 NEXT X
90 PRINT "Center axis color: ";POINT(160,100)
100 PRINT "Plot ready. Press F9 to view."
110 END
