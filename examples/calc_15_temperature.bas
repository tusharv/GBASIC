10 REM Convert Celsius to Fahrenheit: F=C*9/5+32.
20 REM Celsius cannot be below absolute zero (-273.15).
30 INPUT "Temperature in Celsius";C
40 IF C<-273.15 THEN PRINT "Invalid input": END
50 F=C*9/5+32
60 PRINT "Fahrenheit =";F
70 REM Try: compare 0,100,-40. At what temperature do C and F match?
80 END
