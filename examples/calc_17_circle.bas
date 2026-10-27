10 REM Circle area=PI*R^2; circumference=2*PI*R.
20 REM PI=3.14159 is an approximation.
30 INPUT "Radius - positive";R
40 IF R<=0 THEN PRINT "Invalid input": END
50 PI=3.14159
60 A=PI*R^2
70 C=2*PI*R
80 PRINT "Area =";A
90 PRINT "Circumference =";C
100 REM Try: enter 1; then 2. Why does area grow faster than circumference?
110 END
