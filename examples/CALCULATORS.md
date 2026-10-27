# Input-based calculation exercises

These 22 small programs teach INPUT, variables, formulas, arithmetic, validation and IF.
They use the interpreter's existing numbered BASIC subset and run in the ASCII terminal UI.

## How to use them

1. Press **F3** and choose a `calc_` program from the examples dropdown. The dropdown
   supports arrow keys, scrolling and typing a filename prefix to jump to a matching item.
2. Press Enter to select it, then Enter again to open. Press **F5** to run.
3. Read the prompt in Program output. Type **one numeric value** in the bottom INPUT field,
   then press Enter. Repeat for each prompt. Use `10` for 10 percent, not `0.10` or `10%`.
   Do not type currency signs or thousands separators.
4. Read the results, then predict a different result before running again. F6 stops INPUT.
5. Read the REM comments and change one formula as a challenge. Save your version with F4.

All inputs are requested before validation. Out-of-range numeric values print `Invalid input`
and finish. Malformed/non-numeric text produces the interpreter's `Redo from start` error;
it currently ends the run rather than reprompting. Press F5 and try again.

## Simple interest

Open **calc_01_simple_interest.bas**, then enter:

| Prompt | Value |
| --- | --- |
| Principal | 1000 |
| Annual rate percent | 10 |
| Time in years | 2 |

```text
Interest = 200
Total = 1200
```

The formula is `I=P*R*Y/100`; total is `P+I`. Time is in years, so six months is `0.5`.
Change the principal, rate or time one at a time and predict what doubles.

## Compound interest

Open **calc_02_compound_interest.bas** and enter `1000`, `10`, `2`, `1`, one per prompt.
The interest is `210` and total is `1210`.

`A=P*(1+R/(100*F))^(F*Y)`, where R is the nominal annual rate expressed as a percent,
Y is whole years, and F is a positive whole number of compoundings per year. Use F=1
for yearly, F=4 for quarterly, or F=12 for monthly. Compare this result with simple interest.
No fees, taxes, extra deposits or payments are modeled. Zero years and zero rates are allowed.

## The other 20 exercises

Inputs are shown in prompt order. Results below omit BASIC's numeric padding spaces.

| File (all start with `calc_`) | Inputs to try | Expected result / concept |
| --- | --- | --- |
| 03_discount.bas | 1000, 20 | Discount 200; final price 800 |
| 04_sales_tax.bas | 200, 10 | Tax 20; total 220 |
| 05_profit_loss.bas | 100, 120 | Profit 20; change 20% of cost |
| 06_commission.bas | 5000, 5 | Commission 250 |
| 07_salary.bas | 1000, 10, 50 | Base plus 10% allowance, minus 50 deduction; gross 1100, net 1050 |
| 08_savings_goal.bas | 1000, 100, 200 | Remaining 900; round up to 5 months |
| 09_monthly_budget.bas | 2000, 500, 300, 100, 100 | Income, rent, food, transport, other; expenses 1000, balance 1000 |
| 10_bill_split.bas | 100, 10, 2 | Bill plus 10% tip; total 110, each person 55 |
| 11_unit_price.bas | 120, 3 | Cost per unit 40 |
| 12_fuel_cost.bas | 150, 15, 2 | km, km/litre, price/litre; 10 litres, cost 20 |
| 13_average_speed.bas | 150, 3 | km divided by hours; 50 km/h |
| 14_travel_distance.bas | 60, 2 | km/h times hours; 120 km |
| 15_temperature.bas | 37 | Celsius to Fahrenheit; 98.6 F |
| 16_rectangle.bas | 5, 3 | Area 15, perimeter 16 |
| 17_circle.bas | 1 | Area about 3.14159, circumference about 6.28318 |
| 18_triangle_area.bas | 10, 5 | Base and perpendicular height; area 25 |
| 19_cuboid.bas | 4, 3, 2 | Volume 24, total surface area 52 |
| 20_time_conversion.bas | 3661 | 1 hour, 1 minute, 1 second |
| 21_marks_grade.bas | 70, 80, 90 | Three equally weighted subjects out of 100; total 240, average 80%, grade A |
| 22_electricity_bill.bas | 250, 50 | Energy units and fixed charge; energy 500, total 550 |

## Logic and assumptions

- **Percentages:** discount, tax, commission, allowance and tip accept values from 0 to 100.
  For tax and payroll, values are inputs to an arithmetic exercise, not real legal rules.
- **Profit/loss:** percent is based on original cost; loss prints a negative change percent.
  Cost must be positive. A selling price equal to cost prints `No profit or loss`.
- **Salary:** the allowance is a percentage of base salary; deduction is a fixed amount no
  larger than gross salary. No payroll rules are modeled.
- **Savings:** assume equal month-end savings and no interest. Dividing then rounding UP is
  necessary when the target takes a partial month. An already reached goal is handled.
- **Budget:** a negative balance is valid and means expenses exceed income.
- **Splitting:** people must be a positive whole number. Fractions of currency are not rounded
  or allocated between people; this demonstrates division rather than exact accounting.
- **Geometry:** dimensions must be positive and use matching units. Areas are in square units;
  volume is in cubic units. PI=3.14159 is approximate.
- **Time:** input must be nonnegative whole seconds. Hours can exceed 23; this is a duration.
- **Marks:** each input is 0–100. Fictional thresholds are A>=80, B>=60, C>=40, otherwise
  `Needs practice`. Highest thresholds are checked first. This is not an official grading system.
- **Electricity:** invented rates demonstrate progressive slabs: first 100 units at 1.5 each,
  next 100 at 2 each, additional units at 3 each, then add the user-entered fixed charge.
  Only units inside each slab use that slab's rate. These are not current utility prices.

Use modest-sized values. The interpreter uses floating-point arithmetic; results may be
approximate, and large values can overflow. The programs do not implement currency-specific
rounding or arbitrary precision. These are learning exercises, not financial forecasting tools.

## Try building your own

Add a discount before tax; convert Fahrenheit back to Celsius; compare two fuel efficiencies;
add a fourth subject; or print a year-by-year compound-interest table with FOR/NEXT.
Use the [pattern exercises](README.md) to practice loops before combining them with INPUT.
