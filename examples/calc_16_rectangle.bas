10 REM Rectangle area=L*W; perimeter=2*(L+W).
20 REM Use the same length unit for both dimensions.
30 INPUT "Length - positive";L
40 INPUT "Width - positive";W
50 IF L<=0 OR W<=0 THEN PRINT "Invalid input": END
60 PRINT "Area =";L*W
70 PRINT "Perimeter =";2*(L+W)
80 REM Try: enter 5,3. Compare area when both dimensions double.
90 END
