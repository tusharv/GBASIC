10 REM Profit/loss = selling price minus cost price.
20 REM Percent uses COST as the denominator; loss gives a negative change.
30 INPUT "Cost price - positive";C
40 INPUT "Selling price";S
50 IF C<=0 OR S<0 THEN PRINT "Invalid input": END
60 G=S-C
70 IF G>0 THEN PRINT "Profit =";G
80 IF G<0 THEN PRINT "Loss =";-G
90 IF G=0 THEN PRINT "No profit or loss"
100 PRINT "Change percent =";100*G/C
110 REM Try: enter 100,120; then 100,80; then 100,100.
120 END
