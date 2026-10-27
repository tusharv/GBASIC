10 REM A fictional progressive-slab electricity bill.
20 REM First 100 units: 1.5 each; next 100: 2 each; remaining: 3 each.
30 REM These rates are invented for learning, not actual utility prices.
40 INPUT "Energy units used";U
50 INPUT "Fixed charge";FIXED
60 IF U<0 OR FIXED<0 THEN PRINT "Invalid input": END
70 IF U<=100 THEN ENERGY=U*1.5 ELSE ENERGY=150
80 IF U>100 AND U<=200 THEN ENERGY=ENERGY+(U-100)*2
90 IF U>200 THEN ENERGY=ENERGY+200+(U-200)*3
100 PRINT "Energy charge =";ENERGY
110 PRINT "Total bill =";ENERGY+FIXED
120 REM Try: try units 100,101,200,201. Only units in the higher slab use its rate.
130 END
