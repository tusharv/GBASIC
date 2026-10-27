10 REM Compound interest: A=P*(1+R/(100*F))^(F*Y).
20 REM F=1 yearly, F=4 quarterly, F=12 monthly. Rate is nominal annual percent.
30 REM Use whole years and positive whole F. No deposits, fees or taxes.
40 INPUT "Principal";P
50 INPUT "Annual rate percent";R
60 INPUT "Whole years";Y
70 INPUT "Compoundings per year";F
80 IF P<0 OR R<0 OR Y<0 OR Y<>INT(Y) OR F<=0 OR F<>INT(F) THEN PRINT "Invalid input": END
90 A=P*(1+R/(100*F))^(F*Y)
100 I=A-P
110 PRINT "Interest =";I
120 PRINT "Total =";A
130 REM Try: enter 1000,10,2,1. Then compare F=4 or F=12.
140 END
