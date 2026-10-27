10 REM Cuboid volume=L*W*H; surface area=2*(LW+WH+HL).
20 REM Use the same unit for all three dimensions.
30 INPUT "Length - positive";L
40 INPUT "Width - positive";W
50 INPUT "Height - positive";H
60 IF L<=0 OR W<=0 OR H<=0 THEN PRINT "Invalid input": END
70 PRINT "Volume =";L*W*H
80 PRINT "Surface area =";2*(L*W+W*H+H*L)
90 REM Try: enter 4,3,2; then make every dimension 2 to form a cube.
100 END
