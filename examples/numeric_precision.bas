10 REM ! selects single precision; # selects double precision.
20 REM Single precision cannot retain the extra 1 at this magnitude.
30 A#=(16777216!+1!)-16777216!
40 B#=(16777216#+1!)-16777216!
50 PRINT "Single intermediate: ";A#
60 PRINT "Double intermediate: ";B#
70 REM Assigning to double cannot restore rounding lost earlier.
80 REM CDBL converts an already rounded single literal.
90 IF CDBL(2.04)=2.04# THEN PRINT "Same" ELSE PRINT "Literal rounded before CDBL"
100 REM Try replacing the first ! in line 30 with #.
110 END
