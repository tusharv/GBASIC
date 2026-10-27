10 REM Months needed = remaining goal divided by monthly saving, rounded UP.
20 REM Assume no interest and equal month-end savings.
30 INPUT "Savings target";TARGET
40 INPUT "Already saved";SAVED
50 INPUT "Monthly saving - positive";MONTHLY
60 IF TARGET<0 OR SAVED<0 OR MONTHLY<=0 THEN PRINT "Invalid input": END
70 LEFTOVER=TARGET-SAVED
80 IF LEFTOVER<=0 THEN PRINT "Goal already reached": END
90 MONTHS=INT(LEFTOVER/MONTHLY)
100 IF MONTHS*MONTHLY<LEFTOVER THEN MONTHS=MONTHS+1
110 PRINT "Remaining =";LEFTOVER
120 PRINT "Months needed =";MONTHS
130 REM Try: enter 1000,100,200. Why is the answer 5 rather than 4?
140 END
