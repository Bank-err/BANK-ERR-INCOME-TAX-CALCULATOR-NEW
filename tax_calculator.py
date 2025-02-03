import streamlit as st

# Define tax slabs (FY 2025-26)
tax_slabs = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float('inf'), 0.30)  # Above 24 lakh
]

# Standard Deduction for Salaried Individuals
STANDARD_DEDUCTION = 75000

def calculate_tax(income):
    """Calculate income tax based on new tax regime."""
    if income <= STANDARD_DEDUCTION:
        return 0  # No tax if income is below standard deduction
    
    taxable_income = max(0, income - STANDARD_DEDUCTION)  # Apply standard deduction
    total_tax = 0
    previous_limit = 0

    for limit, rate in tax_slabs:
        if taxable_income > previous_limit:
            tax_on_slab = min(taxable_income, limit) - previous_limit
            total_tax += tax_on_slab * rate
        else:
            break
        previous_limit = limit

    # Marginal Relief (if applicable)
    threshold = 1200000  # First major tax jump
    excess_income = taxable_income - threshold

    if excess_income > 0:
        tax_without_relief = total_tax
        marginal_relief = max(0, tax_without_relief - excess_income)
        total_tax -= marginal_relief  # Apply relief

    # Add 4% Health & Education Cess
    total_tax += total_tax * 0.04

    return round(total_tax, 2)

# Streamlit Web App UI
st.title("Income Tax Calculator (New Regime) - FY 2025-26")

income = st.number_input("Enter Your Annual Income (₹)", min_value=0, step=10000)

if st.button("Calculate Tax"):
    tax = calculate_tax(income)
    st.success(f"Your total income tax liability: ₹{tax}")
