10 REM Simple interest: I=P*R*T/100; total=P+I.
20 REM Use nonnegative values. Fractional years are allowed. No fees or payments.
30 INPUT "Principal";P
40 INPUT "Annual rate percent";R
50 INPUT "Time in years";Y
60 IF P<0 OR R<0 OR Y<0 THEN PRINT "Invalid input": END
70 I=P*R*Y/100
80 A=P+I
90 PRINT "Interest =";I
100 PRINT "Total =";A
110 REM Try: enter 1000,10,2. Interest is 200. What if the time doubles?
120 END
