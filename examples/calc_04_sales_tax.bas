10 REM Tax is added to the original price.
20 REM User-supplied arithmetic rate, not a real tax rule.
30 INPUT "Price before tax";P
40 INPUT "Tax percent 0 to 100";R
50 IF P<0 OR R<0 OR R>100 THEN PRINT "Invalid input": END
60 T=P*R/100
70 PRINT "Tax =";T
80 PRINT "Total =";P+T
90 REM Try: enter 200,10. Change the tax rate to zero.
100 END
