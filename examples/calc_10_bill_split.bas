10 REM Add a tip, then split the total equally.
20 REM No currency rounding/remainder allocation; use small inputs.
30 INPUT "Bill amount";BILL
40 INPUT "Tip percent 0 to 100";R
50 INPUT "Number of people";PEOPLE
60 IF BILL<0 OR R<0 OR R>100 OR PEOPLE<=0 OR PEOPLE<>INT(PEOPLE) THEN PRINT "Invalid input": END
70 TIP=BILL*R/100
80 TOTAL=BILL+TIP
90 PRINT "Tip =";TIP
100 PRINT "Total =";TOTAL
110 PRINT "Each person =";TOTAL/PEOPLE
120 REM Try: enter 100,10,2. What changes if 4 people share?
130 END
