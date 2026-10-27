10 REM Average speed = total distance divided by total time.
20 INPUT "Distance in km";D
30 INPUT "Time in hours - positive";T
40 IF D<0 OR T<=0 THEN PRINT "Invalid input": END
50 PRINT "Speed km/h =";D/T
60 REM Try: enter 150,3; then 150,2. Include stop time in total time.
70 END
