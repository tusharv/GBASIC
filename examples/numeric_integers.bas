10 REM Integer calculations promote to single beyond the 16-bit range.
20 PRINT "Promoted sum: ";32767+1
30 PRINT "Promoted product: ";300*300
40 REM A percent-suffixed variable still rejects out-of-range assignment.
50 REM Slash produces a floating-point result even with integer operands.
60 PRINT "Division: ";5/2
70 REM INT rounds downward; FIX truncates toward zero.
80 PRINT "INT: ";INT(-1.5!)
90 PRINT "FIX: ";FIX(-1.5!)
100 REM Try a positive value in lines 80 and 90 and compare.
110 END
