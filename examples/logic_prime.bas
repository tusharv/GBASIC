10 REM Prime test: N is prime if no integer divisor from 2 to SQR(N) divides it.
20 REM MOD gives the remainder. A flag remembers whether a divisor was found.
30 REM Try small whole numbers: 1,2,9,29. Predict before running.
40 N=29
50 ISPRIME=1
60 IF N<2 THEN ISPRIME=0
70 FOR DIVISOR=2 TO INT(SQR(N))
80 IF N MOD DIVISOR=0 THEN ISPRIME=0
90 NEXT DIVISOR
100 IF ISPRIME THEN PRINT "Prime" ELSE PRINT "Not prime"
110 END
