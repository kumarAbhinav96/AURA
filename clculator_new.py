import math
import statistics
import cmath
from typing import Any, List

import sympy as sp
from sympy import SympifyError
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("advanced-calculator-pro")


# -----------------------------
# Helper functions
# -----------------------------
def format_result(value: Any) -> str:
    try:
        return str(sp.simplify(value))
    except Exception:   #f simplification fails, then:
        return str(value)  # just convert the value direct;y into string 
    
    

def parse_expression(expression: str, variable: str = "x"):
    if not isinstance(expression, str) or not expression.strip():  #the string is not empty
        raise ValueError("Expression must be a non-empty string.")

    var = sp.Symbol(variable)
    return sp.sympify(
        expression,
        locals={
            variable: var,
            "x": sp.Symbol("x"),
            "e": sp.E,   #Defines Euler’s number.
            "pi": sp.pi,
            "i": sp.I,   #Defines imaginary unit.
            "oo": sp.oo,  #Defines imaginary unit.
        },
    )


# -----------------------------
# Existing core tools
# -----------------------------
@mcp.tool()
def evaluate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        expr = parse_expression(expression)
        result = expr.evalf()
        return f"Result: {format_result(result)}"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while evaluating expression: {e}"


@mcp.tool()
def derivative(expression: str, variable: str = "x") -> str:
    """Compute symbolic derivative."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expression(expression, variable)
        result = sp.diff(expr, var)
        return f"d/d{variable}({expression}) = {format_result(result)}"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while computing derivative: {e}"


@mcp.tool()
def integral(expression: str, variable: str = "x") -> str:
    """Compute symbolic indefinite integral."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expression(expression, variable)
        result = sp.integrate(expr, var)
        return f"∫({expression}) d{variable} = {format_result(result)} + C"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while computing integral: {e}"


@mcp.tool()
def simplify(expression: str, variable: str = "x") -> str:
    """Simplify expression."""
    try:
        expr = parse_expression(expression, variable)
        result = sp.simplify(expr)
        return f"Simplified: {format_result(result)}"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while simplifying expression: {e}"


@mcp.tool()
def simplify(expression: str, variable: str = "x") -> str:
    """Simplify expression."""
    try:
        expr = parse_expression(expression, variable)
        result = sp.simplify(expr)
        return f"Simplified: {format_result(result)}"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while simplifying expression: {e}"
    
@mcp.tool()
def expand(expression: str, variable: str = "x") -> str:
    """Expand expression."""
    try:
        expr = parse_expression(expression, variable)
        result = sp.expand(expr)
        return f"Expanded: {format_result(result)}"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while expanding expression: {e}"


@mcp.tool()
def factor(expression: str, variable: str = "x") -> str:
    """Factor expression."""
    try:
        expr = parse_expression(expression, variable)
        result = sp.factor(expr)
        return f"Factored: {format_result(result)}"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while factoring expression: {e}"


@mcp.tool()
def solve_equation(equation: str, variable: str = "x") -> str:
    """Solve equation like 'x**2 - 4 = 0' or 'x**2 - 4'."""
    try:
        if not isinstance(equation, str) or not equation.strip():
            return "Error: Equation must be a non-empty string."

        var = sp.Symbol(variable)

        if "=" in equation:
            left, right = equation.split("=", 1)
            eq = sp.Eq(
                parse_expression(left.strip(), variable),
                parse_expression(right.strip(), variable),
            )
        else:
            eq = sp.Eq(parse_expression(equation, variable), 0)

        solutions = sp.solve(eq, var)

        if not solutions:
            return f"No solution found for {equation}"

        return f"Solutions for {equation}: {solutions}"
    except (ValueError, SympifyError) as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error while solving equation: {e}"


@mcp.tool()
def scientific_calculator(operation: str, value: float, degrees: bool = False) -> str:
    """Scientific calculations: sin, cos, tan, log, log10, sqrt, factorial."""
    try:
        operation = operation.lower().strip()

        if operation in {"sin", "cos", "tan"}:
            v = math.radians(value) if degrees else value
            if operation == "sin":
                return f"sin({value}) = {math.sin(v)}"
            if operation == "cos":
                return f"cos({value}) = {math.cos(v)}"
            if operation == "tan":
                return f"tan({value}) = {math.tan(v)}"

        elif operation == "log":
            if value <= 0:
                return "Error: log is only defined for positive numbers"
            return f"log({value}) = {math.log(value)}"

        elif operation == "log10":
            if value <= 0:
                return "Error: log10 is only defined for positive numbers"
            return f"log10({value}) = {math.log10(value)}"

        elif operation == "sqrt":
            if value < 0:
                return "Error: sqrt is not defined for negative real numbers"
            return f"sqrt({value}) = {math.sqrt(value)}"

        elif operation == "factorial":
            if value < 0 or not float(value).is_integer():
                return "Error: factorial requires a non-negative integer"
            return f"factorial({int(value)}) = {math.factorial(int(value))}"

        else:
            return "Error: Unsupported scientific operation"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def matrix_operations(operation: str, matrixA: List[List[float]], matrixB: List[List[float]] = None) -> str:
    """Matrix operations: determinant, inverse, transpose, multiply, add, subtract."""
    try:
        A = sp.Matrix(matrixA)
        operation = operation.lower().strip()

        if operation == "determinant":
            if A.rows != A.cols:
                return "Error: Determinant requires a square matrix"
            return f"Determinant: {A.det()}"

        elif operation == "inverse":
            if A.rows != A.cols:
                return "Error: Inverse requires a square matrix"
            if A.det() == 0:
                return "Error: Matrix is singular, inverse does not exist"
            return f"Inverse:\n{A.inv()}"

        elif operation == "transpose":
            return f"Transpose:\n{A.T}"

        elif operation == "multiply":
            if matrixB is None:
                return "Error: matrixB is required for multiplication"
            B = sp.Matrix(matrixB)
            return f"Product:\n{A * B}"

        elif operation == "add":
            if matrixB is None:
                return "Error: matrixB is required for addition"
            B = sp.Matrix(matrixB)
            return f"Sum:\n{A + B}"

        elif operation == "subtract":
            if matrixB is None:
                return "Error: matrixB is required for subtraction"
            B = sp.Matrix(matrixB)
            return f"Difference:\n{A - B}"

        else:
            return "Error: Unknown matrix operation"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def statistics_tool(data: List[float], operation: str) -> str:
    """Statistics: mean, median, std, variance, min, max, sum."""
    try:
        if not data:
            return "Error: Data list cannot be empty"

        operation = operation.lower().strip()

        if operation == "mean":
            return f"Mean: {statistics.mean(data)}"
        elif operation == "median":
            return f"Median: {statistics.median(data)}"
        elif operation == "std":
            if len(data) < 2:
                return "Error: Standard deviation requires at least 2 values"
            return f"Standard Deviation: {statistics.stdev(data)}"
        elif operation == "variance":
            if len(data) < 2:
                return "Error: Variance requires at least 2 values"
            return f"Variance: {statistics.variance(data)}"
        elif operation == "min":
            return f"Min: {min(data)}"
        elif operation == "max":
            return f"Max: {max(data)}"
        elif operation == "sum":
            return f"Sum: {sum(data)}"
        else:
            return "Error: Unknown statistics operation"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Basic unit conversion."""
    try:
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        if from_unit == "m" and to_unit == "km":
            return f"{value} m = {value / 1000} km"
        elif from_unit == "km" and to_unit == "m":
            return f"{value} km = {value * 1000} m"
        elif from_unit == "celsius" and to_unit == "fahrenheit":
            return f"{value} °C = {(value * 9/5) + 32} °F"
        elif from_unit == "fahrenheit" and to_unit == "celsius":
            return f"{value} °F = {(value - 32) * 5/9} °C"
        else:
            return "Error: Unsupported unit conversion"
    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# 15 additional tools
# -----------------------------

# 1
@mcp.tool()
def definite_integral(expression: str, lower: float, upper: float, variable: str = "x") -> str:
    """Compute definite integral."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expression(expression, variable)
        result = sp.integrate(expr, (var, lower, upper))
        return f"∫[{lower}, {upper}] {expression} d{variable} = {format_result(result)}"
    except Exception as e:
        return f"Error: {e}"


# 2
@mcp.tool()
def limit_tool(expression: str, variable: str = "x", point: str = "0", direction: str = "+") -> str:
    """Compute limit of expression."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expression(expression, variable)
        p = sp.sympify(point)
        result = sp.limit(expr, var, p, dir=direction)
        return f"lim {variable}->{point} of {expression} = {format_result(result)}"
    except Exception as e:
        return f"Error: {e}"


# 3
@mcp.tool()
def solve_linear(a: float, b: float, c: float) -> str:
    """Solve ax + b = c."""
    try:
        if a == 0:
            if b == c:
                return "Infinite solutions"
            return "No solution"
        x = (c - b) / a
        return f"{a}x + {b} = {c} => x = {x}"
    except Exception as e:
        return f"Error: {e}"


# 4
@mcp.tool()
def solve_quadratic(a: float, b: float, c: float) -> str:
    """Solve ax^2 + bx + c = 0."""
    try:
        if a == 0:
            return "Error: a cannot be 0 in a quadratic equation"
        x = sp.Symbol("x")
        expr = a * x**2 + b * x + c
        roots = sp.solve(expr, x)
        return f"Roots: {roots}"
    except Exception as e:
        return f"Error: {e}"


# 5
@mcp.tool()
def polynomial_roots(coefficients: List[float]) -> str:
    """Find roots of a polynomial from coefficient list."""
    try:
        if not coefficients or len(coefficients) < 2:
            return "Error: Provide at least 2 coefficients"
        x = sp.Symbol("x")
        poly = sum(coef * x**(len(coefficients) - i - 1) for i, coef in enumerate(coefficients))
        roots = sp.solve(poly, x)
        return f"Polynomial: {poly}\nRoots: {roots}"
    except Exception as e:
        return f"Error: {e}"


# 6
@mcp.tool()
def complex_number_tool(operation: str, a_real: float, a_imag: float, b_real: float = 0, b_imag: float = 0) -> str:
    """Complex number operations: add, subtract, multiply, divide, modulus, argument, conjugate."""
    try:
        operation = operation.lower().strip()
        z1 = complex(a_real, a_imag)
        z2 = complex(b_real, b_imag)

        if operation == "add":
            result = z1 + z2
        elif operation == "subtract":
            result = z1 - z2
        elif operation == "multiply":
            result = z1 * z2
        elif operation == "divide":
            if z2 == 0:
                return "Error: Cannot divide by zero"
            result = z1 / z2
        elif operation == "modulus":
            result = abs(z1)
        elif operation == "argument":
            result = cmath.phase(z1)
        elif operation == "conjugate":
            result = z1.conjugate()
        else:
            return "Error: Unsupported complex operation"

        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"


# 7
@mcp.tool()
def number_theory_tool(operation: str, a: int, b: int = 0) -> str:
    """Number theory: gcd, lcm, is_prime, prime_factors, fibonacci, combinations, permutations."""
    try:
        operation = operation.lower().strip()

        if operation == "gcd":
            return f"GCD({a}, {b}) = {math.gcd(a, b)}"

        elif operation == "lcm":
            return f"LCM({a}, {b}) = {math.lcm(a, b)}"

        elif operation == "is_prime":
            return f"{a} is {'prime' if sp.isprime(a) else 'not prime'}"

        elif operation == "prime_factors":
            return f"Prime factors of {a}: {sp.factorint(a)}"

        elif operation == "fibonacci":
            if a < 0:
                return "Error: Fibonacci requires non-negative integer"
            fib = [0, 1]
            for _ in range(2, a + 1):
                fib.append(fib[-1] + fib[-2])
            return f"Fibonacci({a}) = {fib[a]}"

        elif operation == "combinations":
            return f"C({a}, {b}) = {math.comb(a, b)}"

        elif operation == "permutations":
            return f"P({a}, {b}) = {math.perm(a, b)}"

        else:
            return "Error: Unsupported number theory operation"
    except Exception as e:
        return f"Error: {e}"


# 8
@mcp.tool()
def percentage_tool(operation: str, value1: float, value2: float, value3: float = 0) -> str:
    """Percentage and finance utilities: percentage, profit_loss, simple_interest, compound_interest, ratio_split."""
    try:
        operation = operation.lower().strip()

        if operation == "percentage":
            return f"{value1}% of {value2} = {(value1 / 100) * value2}"

        elif operation == "profit_loss":
            cp = value1
            spv = value2
            diff = spv - cp
            pct = abs(diff) / cp * 100 if cp != 0 else 0
            if diff > 0:
                return f"Profit = {diff}, Profit% = {pct}"
            elif diff < 0:
                return f"Loss = {abs(diff)}, Loss% = {pct}"
            else:
                return "No profit, no loss"

        elif operation == "simple_interest":
            p, r, t = value1, value2, value3
            si = (p * r * t) / 100
            return f"Simple Interest = {si}"

        elif operation == "compound_interest":
            p, r, t = value1, value2, value3
            amount = p * ((1 + r / 100) ** t)
            ci = amount - p
            return f"Compound Interest = {ci}, Amount = {amount}"

        elif operation == "ratio_split":
            total = value1
            ratio1 = value2
            ratio2 = value3
            if ratio1 + ratio2 == 0:
                return "Error: Ratio sum cannot be zero"
            part1 = total * ratio1 / (ratio1 + ratio2)
            part2 = total * ratio2 / (ratio1 + ratio2)
            return f"Split: {part1} and {part2}"

        else:
            return "Error: Unsupported percentage tool operation"
    except Exception as e:
        return f"Error: {e}"


# 9
@mcp.tool()
def logarithm_base(value: float, base: float) -> str:
    """Compute logarithm with custom base."""
    try:
        if value <= 0:
            return "Error: Value must be positive"
        if base <= 0 or base == 1:
            return "Error: Base must be positive and not equal to 1"
        result = math.log(value, base)
        return f"log base {base} of {value} = {result}"
    except Exception as e:
        return f"Error: {e}"


# 10
@mcp.tool()
def advanced_matrix_tool(operation: str, matrixA: List[List[float]]) -> str:
    """Advanced matrix operations: rank, trace, eigenvalues, eigenvectors, adjoint."""
    try:
        A = sp.Matrix(matrixA)
        operation = operation.lower().strip()

        if operation == "rank":
            return f"Rank: {A.rank()}"

        elif operation == "trace":
            if A.rows != A.cols:
                return "Error: Trace requires square matrix"
            return f"Trace: {A.trace()}"

        elif operation == "eigenvalues":
            if A.rows != A.cols:
                return "Error: Eigenvalues require square matrix"
            return f"Eigenvalues: {A.eigenvals()}"

        elif operation == "eigenvectors":
            if A.rows != A.cols:
                return "Error: Eigenvectors require square matrix"
            return f"Eigenvectors: {A.eigenvects()}"

        elif operation == "adjoint":
            if A.rows != A.cols:
                return "Error: Adjoint requires square matrix"
            return f"Adjoint:\n{A.adjugate()}"

        else:
            return "Error: Unsupported advanced matrix operation"
    except Exception as e:
        return f"Error: {e}"


# 11
@mcp.tool()
def advanced_statistics_tool(data: List[float], operation: str, percentile_value: float = 50) -> str:
    """Advanced statistics: mode, range, percentile, quartiles."""
    try:
        if not data:
            return "Error: Data list cannot be empty"

        operation = operation.lower().strip()
        sorted_data = sorted(data)

        if operation == "mode":
            return f"Mode: {statistics.multimode(data)}"

        elif operation == "range":
            return f"Range: {max(data) - min(data)}"

        elif operation == "percentile":
            if not (0 <= percentile_value <= 100):
                return "Error: Percentile must be between 0 and 100"
            k = (len(sorted_data) - 1) * percentile_value / 100
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                result = sorted_data[int(k)]
            else:
                result = sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)
            return f"{percentile_value}th percentile: {result}"

        elif operation == "quartiles":
            q2 = statistics.median(sorted_data)
            mid = len(sorted_data) // 2
            if len(sorted_data) % 2 == 0:
                lower = sorted_data[:mid]
                upper = sorted_data[mid:]
            else:
                lower = sorted_data[:mid]
                upper = sorted_data[mid + 1:]
            q1 = statistics.median(lower)
            q3 = statistics.median(upper)
            return f"Quartiles: Q1={q1}, Q2={q2}, Q3={q3}"

        else:
            return "Error: Unsupported advanced statistics operation"
    except Exception as e:
        return f"Error: {e}"


# 12
@mcp.tool()
def advanced_unit_conversion(value: float, from_unit: str, to_unit: str) -> str:
    """Advanced unit conversion for length, weight, speed, time."""
    try:
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        conversions = {
            "m": 1,
            "km": 1000,
            "cm": 0.01,
            "mm": 0.001,
            "g": 1,
            "kg": 1000,
            "mg": 0.001,
            "s": 1,
            "min": 60,
            "h": 3600,
            "mps": 1,
            "kmph": 1000 / 3600,
        }

        if from_unit in conversions and to_unit in conversions:
            base_value = value * conversions[from_unit]
            result = base_value / conversions[to_unit]
            return f"{value} {from_unit} = {result} {to_unit}"

        return "Error: Unsupported advanced unit conversion"
    except Exception as e:
        return f"Error: {e}"


# 13
@mcp.tool()
def base_conversion(value: str, from_base: int, to_base: int) -> str:
    """Convert numbers between bases 2, 8, 10, 16."""
    try:
        decimal_value = int(value, from_base)

        if to_base == 2:
            result = bin(decimal_value)[2:]
        elif to_base == 8:
            result = oct(decimal_value)[2:]
        elif to_base == 10:
            result = str(decimal_value)
        elif to_base == 16:
            result = hex(decimal_value)[2:]
        else:
            return "Error: Supported target bases are 2, 8, 10, 16"

        return f"{value} (base {from_base}) = {result} (base {to_base})"
    except Exception as e:
        return f"Error: {e}"


# 14
@mcp.tool()
def compare_expressions(expr1: str, expr2: str, variable: str = "x") -> str:
    """Check whether two expressions are mathematically equivalent."""
    try:
        e1 = parse_expression(expr1, variable)
        e2 = parse_expression(expr2, variable)
        diff = sp.simplify(e1 - e2)
        if diff == 0:
            return "Expressions are equivalent"
        return f"Expressions are not equivalent. Difference: {diff}"
    except Exception as e:
        return f"Error: {e}"


# 15
@mcp.tool()
def series_expansion(expression: str, variable: str = "x", point: float = 0, order: int = 6) -> str:
    """Compute Taylor/Maclaurin series expansion."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expression(expression, variable)
        result = sp.series(expr, var, point, order)
        return f"Series expansion of {expression} around {variable}={point} up to order {order}:\n{result}"
    except Exception as e:
        return f"Error: {e}"


# 16 bonus from earlier suggestion
@mcp.tool()
def solve_system_of_equations(equations: List[str], variables: List[str]) -> str:
    """Solve a system of algebraic equations."""
    try:
        if not equations or not variables:
            return "Error: equations and variables cannot be empty"

        vars_symbols = [sp.Symbol(v) for v in variables]
        eq_list = []

        for eq in equations:
            if "=" in eq:
                left, right = eq.split("=", 1)
                eq_obj = sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
            else:
                eq_obj = sp.Eq(sp.sympify(eq.strip()), 0)
            eq_list.append(eq_obj)

        result = sp.solve(eq_list, vars_symbols, dict=True)
        return f"Solutions: {result}"
    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# Run server
# # -----------------------------
# if __name__ == "__main__":
#     mcp.run()


# print(evaluate("2+3*4"))
# print(derivative("x**2 + 3*x"))
# print(integral("x"))
# print(simplify("2*x + 3*x - x"))
# print(definite_integral("x**2", 0, 2))


if __name__ == "__main__":
    test_mode = True   # change to False for MCP

    if test_mode:
        print(evaluate("2+3*4"))
        print(derivative("x**2 + 3*x"))
        print(integral("x"))
        print(simplify("2*x + 3*x - x"))
        print(definite_integral("x**2", 0, 2))
    else:
        mcp.run()