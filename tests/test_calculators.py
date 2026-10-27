from io import StringIO
from pathlib import Path

import pytest

from ghost_basic import Program, Runtime
from ghost_basic.devices import Disk

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"

# Hand-calculated results, independent of the formulas in the BASIC programs.
CASES = [
    ("01_simple_interest", "1000\n10\n2\n", "Interest = 200 \nTotal = 1200 \n", "-1\n10\n2\n"),
    (
        "02_compound_interest",
        "1000\n10\n2\n1\n",
        "Interest = 210 \nTotal = 1210 \n",
        "1000\n10\n2\n0\n",
    ),
    ("03_discount", "1000\n20\n", "Discount = 200 \nFinal price = 800 \n", "1000\n101\n"),
    ("04_sales_tax", "200\n10\n", "Tax = 20 \nTotal = 220 \n", "200\n-1\n"),
    ("05_profit_loss", "100\n120\n", "Profit = 20 \nChange percent = 20 \n", "0\n120\n"),
    ("06_commission", "5000\n5\n", "Commission = 250 \n", "5000\n-1\n"),
    (
        "07_salary",
        "1000\n10\n50\n",
        "Gross salary = 1100 \nNet salary = 1050 \n",
        "1000\n10\n1200\n",
    ),
    (
        "08_savings_goal",
        "1000\n100\n200\n",
        "Remaining = 900 \nMonths needed = 5 \n",
        "1000\n100\n0\n",
    ),
    (
        "09_monthly_budget",
        "2000\n500\n300\n100\n100\n",
        "Expenses = 1000 \nBalance = 1000 \n",
        "2000\n500\n-1\n100\n100\n",
    ),
    (
        "10_bill_split",
        "100\n10\n2\n",
        "Tip = 10 \nTotal = 110 \nEach person = 55 \n",
        "100\n10\n0\n",
    ),
    ("11_unit_price", "120\n3\n", "Unit price = 40 \n", "120\n0\n"),
    ("12_fuel_cost", "150\n15\n2\n", "Litres needed = 10 \nFuel cost = 20 \n", "150\n0\n2\n"),
    ("13_average_speed", "150\n3\n", "Speed km/h = 50 \n", "150\n0\n"),
    ("14_travel_distance", "60\n2\n", "Distance km = 120 \n", "-1\n2\n"),
    ("15_temperature", "37\n", "Fahrenheit = 98.6 \n", "-274\n"),
    ("16_rectangle", "5\n3\n", "Area = 15 \nPerimeter = 16 \n", "-1\n3\n"),
    ("17_circle", "1\n", "Area = 3.14159 \nCircumference = 6.28318 \n", "-1\n"),
    ("18_triangle_area", "10\n5\n", "Area = 25 \n", "10\n-1\n"),
    ("19_cuboid", "4\n3\n2\n", "Volume = 24 \nSurface area = 52 \n", "4\n0\n2\n"),
    ("20_time_conversion", "3661\n", "Hours = 1 \nMinutes = 1 \nSeconds = 1 \n", "1.5\n"),
    (
        "21_marks_grade",
        "70\n80\n90\n",
        "Total = 240 \nAverage percent = 80 \nGrade = A\n",
        "101\n80\n90\n",
    ),
    ("22_electricity_bill", "250\n50\n", "Energy charge = 500 \nTotal bill = 550 \n", "-1\n50\n"),
]


def run_calculator(name, inputs):
    output = StringIO()
    stream = StringIO(inputs)
    Runtime(output=output, input_stream=stream).run(
        Program.from_source((EXAMPLES / f"calc_{name}.bas").read_text())
    )
    assert stream.read() == "", "Every supplied input should be consumed"
    return output.getvalue()


@pytest.mark.parametrize("name, inputs, expected, invalid", CASES, ids=[c[0] for c in CASES])
def test_calculator_results(name, inputs, expected, invalid):
    output = run_calculator(name, inputs)
    assert output.endswith(expected)
    assert "Invalid input" not in output
    assert f"examples/calc_{name}.bas" in Disk(EXAMPLES.parent).example_programs()


@pytest.mark.parametrize("name, inputs, expected, invalid", CASES, ids=[c[0] for c in CASES])
def test_calculator_rejects_invalid_values(name, inputs, expected, invalid):
    assert run_calculator(name, invalid).endswith("Invalid input\n")


@pytest.mark.parametrize(
    "name, inputs, expected",
    [
        ("01_simple_interest", "1000\n0\n2\n", "Interest = 0 \nTotal = 1000 \n"),
        ("02_compound_interest", "1000\n10\n0\n12\n", "Interest = 0 \nTotal = 1000 \n"),
        ("02_compound_interest", "1000\n100\n1\n2\n", "Interest = 1250 \nTotal = 2250 \n"),
        ("02_compound_interest", "1000\n10\n1\n1.5\n", "Invalid input\n"),
        ("05_profit_loss", "100\n80\n", "Loss = 20 \nChange percent =-20 \n"),
        ("05_profit_loss", "100\n100\n", "No profit or loss\nChange percent = 0 \n"),
        ("08_savings_goal", "1000\n200\n200\n", "Remaining = 800 \nMonths needed = 4 \n"),
        ("08_savings_goal", "1000\n1100\n200\n", "Goal already reached\n"),
        ("09_monthly_budget", "100\n100\n50\n0\n0\n", "Expenses = 150 \nBalance =-50 \n"),
        ("10_bill_split", "100\n10\n2.5\n", "Invalid input\n"),
        ("15_temperature", "-40\n", "Fahrenheit =-40 \n"),
        ("20_time_conversion", "0\n", "Hours = 0 \nMinutes = 0 \nSeconds = 0 \n"),
        ("21_marks_grade", "60\n60\n60\n", "Total = 180 \nAverage percent = 60 \nGrade = B\n"),
        ("21_marks_grade", "40\n40\n40\n", "Total = 120 \nAverage percent = 40 \nGrade = C\n"),
        (
            "21_marks_grade",
            "39\n39\n39\n",
            "Total = 117 \nAverage percent = 39 \nGrade = Needs practice\n",
        ),
        ("22_electricity_bill", "100\n50\n", "Energy charge = 150 \nTotal bill = 200 \n"),
        ("22_electricity_bill", "200\n50\n", "Energy charge = 350 \nTotal bill = 400 \n"),
        ("22_electricity_bill", "0\n50\n", "Energy charge = 0 \nTotal bill = 50 \n"),
    ],
)
def test_calculator_boundaries(name, inputs, expected):
    assert run_calculator(name, inputs).endswith(expected)


@pytest.mark.asyncio
async def test_compound_interest_inputs_in_terminal_ui():
    from textual.widgets import Input

    from ghost_basic.tui import GhostBasicApp

    app = GhostBasicApp(root=EXAMPLES.parent, filename="examples/calc_02_compound_interest.bas")
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("f5")
        for value in ("1000", "10", "2", "1"):
            for _ in range(100):
                await pilot.pause(0.01)
                if app.waiting_input:
                    break
            assert app.waiting_input
            field = app.query_one("#command", Input)
            field.value = value
            field.focus()
            await pilot.press("enter")
        for _ in range(100):
            await pilot.pause(0.01)
            if not app.runner.running:
                app.poll_execution()
                break
        assert not app.runner.running
        assert app.output_text.endswith("Interest = 210 \nTotal = 1210 \n")
