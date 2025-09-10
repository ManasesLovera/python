#!/usr/bin/env python3
"""
Python IS Excellent for Precision Work - Comprehensive Demonstration
"""

def main():
    print("=== PYTHON IS GREAT FOR PRECISION WORK ===\n")

    print("1. DECIMAL MODULE - Exact Decimal Arithmetic")
    from decimal import Decimal, getcontext
    getcontext().prec = 50  # Set very high precision

    # Financial calculations with perfect precision
    account_balance = Decimal('1234.56')
    interest_rate = Decimal('0.05')  # 5%
    interest = account_balance * interest_rate
    new_balance = account_balance + interest

    print(f"   Account: ${account_balance}")
    print(f"   Interest (5%): ${interest}")
    print(f"   New Balance: ${new_balance}")
    print(f"   Perfect precision: {new_balance == Decimal('1296.288')}")

    print("\n2. FRACTIONS MODULE - Exact Rational Arithmetic")
    from fractions import Fraction

    # Exact fractions - no precision loss
    f1 = Fraction(1, 3)  # 1/3
    f2 = Fraction(1, 6)  # 1/6
    f3 = f1 + f2
    print(f"   1/3 + 1/6 = {f3} = {float(f3)}")
    print(f"   Exact result: {f3 == Fraction(1, 2)}")

    print("\n3. NUMPY - High Precision Numerical Computing")
    import numpy as np

    # Numpy with high precision
    a = np.array([0.1, 0.2, 0.3], dtype=np.float64)
    result = np.sum(a)
    print(f"   Numpy sum: {result}")
    print(f"   Using isclose: {np.isclose(result, 0.6)}")

    print("\n4. PRACTICAL EXAMPLES - When Precision Matters")

    print("\n   A. Financial Calculations:")
    # Banking system - must be exact
    principal = Decimal('10000.00')
    rate = Decimal('0.045')  # 4.5%
    time = Decimal('2.5')
    interest = principal * rate * time
    total = principal + interest
    print(f"      Principal: ${principal}")
    print(f"      Interest: ${interest}")
    print(f"      Total: ${total}")
    print(f"      Exact calculation: {total == Decimal('11125.00')}")

    print("\n   B. Statistical Analysis:")
    # Statistical calculations with proper precision
    data = [1.1, 2.2, 3.3, 4.4, 5.5]
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    print(f"      Data: {data}")
    print(f"      Mean: {mean}")
    print(f"      Std Dev: {std}")
    print(f"      Using numpy for reliable statistics")

    print("\n   C. Engineering Calculations:")
    # Engineering precision
    pi = Decimal('3.141592653589793238462643383279')
    radius = Decimal('5.0')
    area = pi * radius * radius
    circumference = 2 * pi * radius
    print(f"      Radius: {radius} units")
    print(f"      Area: {area} square units")
    print(f"      Circumference: {circumference} units")
    print(f"      Exact geometric calculations!")

    print("\n5. COMPARISON WITH OTHER LANGUAGES")
    print("   Python's precision tools are often BETTER than other languages:")
    print("   - JavaScript: No built-in decimal type")
    print("   - C/C++: Requires external libraries")
    print("   - Java: BigDecimal available but more verbose")
    print("   - Python: Decimal, Fractions, Numpy built-in or standard library")

    print("\n6. WHEN TO USE EACH TOOL")
    print("   🏦 Financial calculations → Decimal")
    print("   📊 Scientific computing → Numpy")
    print("   🔢 Exact fractions → Fractions")
    print("   🧮 Symbolic math → Sympy")
    print("   📈 Statistics → Numpy/Scipy")
    print("   ⚖️  Measurements with uncertainty → Uncertainties library")

    print("\n=== CONCLUSION ===")
    print("Python is EXCELLENT for precision work because:")
    print("✅ Decimal module for exact decimal arithmetic")
    print("✅ Fractions module for exact rational arithmetic")
    print("✅ Numpy for high-precision numerical computing")
    print("✅ Built-in tools for proper floating-point comparisons")
    print("✅ Rich ecosystem of scientific computing libraries")
    print("✅ Easy to use and understand")
    print("\nThe key is choosing the right tool for your specific needs!")
    print("\nDon't avoid Python for precision work - embrace it with the right tools!")

if __name__ == "__main__":
    main()