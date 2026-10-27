10 REM Add expenses; balance = income minus total expenses.
20 REM A negative balance means expenses exceed income.
30 INPUT "Monthly income";INCOME
40 INPUT "Rent";RENT
50 INPUT "Food";FOOD
60 INPUT "Transport";TRAVEL
70 INPUT "Other expenses";OTHER
80 IF INCOME<0 OR RENT<0 OR FOOD<0 OR TRAVEL<0 OR OTHER<0 THEN PRINT "Invalid input": END
90 EXPENSES=RENT+FOOD+TRAVEL+OTHER
100 PRINT "Expenses =";EXPENSES
110 PRINT "Balance =";INCOME-EXPENSES
120 REM Try: enter 2000,500,300,100,100. Increase rent until balance is negative.
130 END
