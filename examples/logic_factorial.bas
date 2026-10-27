10 REM Factorial: multiply all whole numbers from 1 to N.
20 REM A multiplication accumulator must start at 1, not 0.
30 REM Keep N between 0 and 10 in this beginner exercise.
40 N=5
50 ANSWER=1
60 FOR I=1 TO N
70 ANSWER=ANSWER*I
80 NEXT I
90 PRINT MID$(STR$(N),2);"! =";ANSWER
100 REM Try N=0. Why is the answer 1 even though the loop is skipped?
110 END
