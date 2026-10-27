10 REM Triangle area = base*perpendicular height/2.
20 REM Use matching units; height must be perpendicular to the base.
30 INPUT "Base - positive";B
40 INPUT "Perpendicular height - positive";H
50 IF B<=0 OR H<=0 THEN PRINT "Invalid input": END
60 PRINT "Area =";B*H/2
70 REM Try: enter 10,5. What happens if base is halved?
80 END
