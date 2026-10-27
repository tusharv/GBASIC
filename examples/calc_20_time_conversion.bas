10 REM Split a whole number of seconds into hours, minutes and seconds.
20 REM Hours may exceed 23; this is a duration, not a clock time.
30 INPUT "Total whole seconds";T
40 IF T<0 OR T<>INT(T) THEN PRINT "Invalid input": END
50 H=INT(T/3600)
60 LEFTOVER=T-H*3600
70 M=INT(LEFTOVER/60)
80 S=LEFTOVER-M*60
90 PRINT "Hours =";H
100 PRINT "Minutes =";M
110 PRINT "Seconds =";S
120 REM Try: try 3661,3600,59,0. Why is the leftover always less than 60?
130 END
