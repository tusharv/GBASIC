10 REM Gross = base plus allowance; net = gross minus deduction.
20 REM A fictional allowance and fixed deduction; no payroll or income-tax rules.
30 INPUT "Base salary";B
40 INPUT "Allowance percent 0 to 100";R
50 INPUT "Fixed deduction";D
60 IF B<0 OR R<0 OR R>100 OR D<0 OR D>B*(1+R/100) THEN PRINT "Invalid input": END
70 G=B+B*R/100
80 PRINT "Gross salary =";G
90 PRINT "Net salary =";G-D
100 REM Try: enter 1000,10,50. What happens if allowance is zero?
110 END
