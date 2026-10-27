10 REM Litres = distance/efficiency; cost = litres*price per litre.
20 REM Assumes constant efficiency and price for the entire trip.
30 INPUT "Distance in km";D
40 INPUT "Efficiency in km per litre";E
50 INPUT "Price per litre";P
60 IF D<0 OR E<=0 OR P<0 THEN PRINT "Invalid input": END
70 L=D/E
80 PRINT "Litres needed =";L
90 PRINT "Fuel cost =";L*P
100 REM Try: enter 150,15,2. Predict the cost if distance doubles.
110 END
