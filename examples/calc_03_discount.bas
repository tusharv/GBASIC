10 REM Discount amount = price*percent/100.
20 INPUT "Original price";P
30 INPUT "Discount percent 0 to 100";R
40 IF P<0 OR R<0 OR R>100 THEN PRINT "Invalid input": END
50 D=P*R/100
60 FINAL=P-D
70 PRINT "Discount =";D
80 PRINT "Final price =";FINAL
90 REM Try: enter 1000,20. Compare one 20 percent discount with two 10 percent discounts.
100 END
