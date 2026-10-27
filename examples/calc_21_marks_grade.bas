10 REM Total, average percentage and an example grade for three subjects.
20 REM Fictional thresholds: A>=80, B>=60, C>=40. All subjects equally weighted.
30 INPUT "Subject 1 mark out of 100";A
40 INPUT "Subject 2 mark out of 100";B
50 INPUT "Subject 3 mark out of 100";C
60 IF A<0 OR A>100 OR B<0 OR B>100 OR C<0 OR C>100 THEN PRINT "Invalid input": END
70 TOTAL=A+B+C
80 AVERAGE=TOTAL/3
90 PRINT "Total =";TOTAL
100 PRINT "Average percent =";AVERAGE
110 IF AVERAGE>=80 THEN PRINT "Grade = A": END
120 IF AVERAGE>=60 THEN PRINT "Grade = B": END
130 IF AVERAGE>=40 THEN PRINT "Grade = C": END
140 PRINT "Grade = Needs practice"
150 REM Try: try averages of exactly 80,60,40,39. Why test thresholds from high to low?
160 END
