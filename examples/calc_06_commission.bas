10 REM Commission = sales*commission percent/100.
20 INPUT "Sales amount";S
30 INPUT "Commission percent 0 to 100";R
40 IF S<0 OR R<0 OR R>100 THEN PRINT "Invalid input": END
50 C=S*R/100
60 PRINT "Commission =";C
70 REM Try: enter 5000,5. What sales give commission 500?
80 END
