10 REM Unit price = total cost divided by quantity.
20 INPUT "Total cost";COST
30 INPUT "Quantity - positive";Q
40 IF COST<0 OR Q<=0 THEN PRINT "Invalid input": END
50 PRINT "Unit price =";COST/Q
60 REM Try: compare 120 for 3 units with 180 for 5 units.
70 END
