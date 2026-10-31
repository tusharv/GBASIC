10 REM Connect polar-coordinate samples to draw a spiral.
20 REM F5 run, F9 preview. Change I/30 to I/20 for more turns.
30 SCREEN 7
40 PX=160: PY=100
50 FOR I=1 TO 720
60 T=I/30
70 R=I/8
80 X=160+R*COS(T): Y=100+R*SIN(T)
90 C=9+(I\120) MOD 7
100 LINE (PX,PY)-(X,Y),C
110 PX=X: PY=Y
120 NEXT I
130 PRINT "Spiral ready. Press F9 to view."
140 END
