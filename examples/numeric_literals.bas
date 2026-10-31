10 REM Signed 16-bit hex and octal literals all describe the same bits.
20 REM Try &H7FFF (32767) and &H8000 (-32768).
30 PRINT "Hex: ";&HFFFF
40 PRINT "Octal: ";&O177777
50 PRINT "Short octal: ";&177777
60 REM AND keeps just the low eight bits of the signed value.
70 PRINT "Mask: ";(&HFFFF AND 255)
80 END
