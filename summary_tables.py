import numpy as np
import pandas as pd
from vaccine_mandate_model import VaccineMandateModel

def format_currency(value):
    """Format a numeric value as a currency string"""
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f} billion"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f} million"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f} thousand"
    else:
        return f"${value:.2f}"

def print_baseline_decision(model):
    """Print baseline decision table"""
    decision, util_mandate, util_voluntary = model.make_decision()
    
    print("=== Baseline Decision ===")
    print("\nParameters:")
    for key, value in model.params.items():
        # Format the value appropriately
        if "value" in key or "cost" in key:
            print(f"{key}: {format_currency(value)}")
        elif key in ["vaccine_efficacy", "voluntary_adoption", "mandate_adoption"]:
            print(f"{key}: {value*100:.1f}%")
        else:
            print(f"{key}: {value}")
    
    print("\nDecision Results:")
    print(f"Policy recommendation: {'Mandate' if decision else 'Voluntary'}")
    print(f"Utility with mandate: {format_currency(util_mandate)}")
    print(f"Utility without mandate: {format_currency(util_voluntary)}")
    print(f"Utility difference: {format_currency(util_mandate - util_voluntary)}")

def print_sensitivity_table(model, parameter, values, title):
    """Print sensitivity analysis for a parameter"""
    results = model.sensitivity_analysis(parameter, values)
    
    # Format the values for display
    formatted_results = []
    for _, row in results.iterrows():
        if parameter in ["vaccine_efficacy", "voluntary_adoption", "mandate_adoption"]:
            param_value = f"{row['value']*100:.1f}%"
        elif "value" in parameter or "cost" in parameter:
            param_value = format_currency(row['value'])
        else:
            param_value = f"{row['value']}"
            
        formatted_results.append({
            "Parameter Value": param_value,
            "Decision": row['decision'],
            "Utility Difference": format_currency(row['utility_difference'])
        })
    
    # Create a DataFrame for pretty printing
    df = pd.DataFrame(formatted_results)
    
    print(f"\n=== {title} ===")
    print(df.to_string(index=False))

def print_two_way_table(model, param1, values1, param2, values2, title):
    """Print two-way sensitivity analysis table"""
    results = model.two_way_analysis(param1, values1, param2, values2)
    
    # Format the values in the pivot table
    pivot_table = results.pivot(index=param1, columns=param2, values="decision")
    
    # Format row and column headers
    new_index = []
    for val in pivot_table.index:
        if "value" in param1 or "cost" in param1:
            new_index.append(format_currency(val))
        elif param1 in ["vaccine_efficacy", "voluntary_adoption", "mandate_adoption"]:
            new_index.append(f"{val*100:.1f}%")
        else:
            new_index.append(str(val))
    
    new_columns = []
    for val in pivot_table.columns:
        if "value" in param2 or "cost" in param2:
            new_columns.append(format_currency(val))
        elif param2 in ["vaccine_efficacy", "voluntary_adoption", "mandate_adoption"]:
            new_columns.append(f"{val*100:.1f}%")
        else:
            new_columns.append(str(val))
    
    # Create a new DataFrame with formatted headers
    formatted_table = pd.DataFrame(
        pivot_table.values,
        index=new_index,
        columns=new_columns
    )
    
    print(f"\n=== {title} ===")
    print(formatted_table.to_string())

if __name__ == "__main__":
    model = VaccineMandateModel()
    
    # Print baseline decision
    print_baseline_decision(model)
    
    # Print sensitivity tables
    print_sensitivity_table(
        model,
        "vaccine_efficacy",
        np.linspace(0.5, 0.95, 6),
        "Sensitivity to Vaccine Efficacy"
    )
    
    print_sensitivity_table(
        model,
        "freedom_value",
        [100000000, 200000000, 300000000, 400000000, 500000000],
        "Sensitivity to Freedom Value"
    )
    
    print_sensitivity_table(
        model,
        "mandate_adoption",
        np.linspace(0.65, 0.95, 5),
        "Sensitivity to Mandate Adoption Rate"
    )
    
    # Print two-way sensitivity tables
    print_two_way_table(
        model,
        "freedom_value",
        [100000000, 200000000, 300000000, 400000000],
        "vaccine_efficacy",
        [0.7, 0.8, 0.9, 0.95],
        "Two-way Analysis: Freedom Value vs. Vaccine Efficacy"
    )
    
    print_two_way_table(
        model,
        "enforcement_cost",
        [50000000, 100000000, 150000000, 200000000],
        "mandate_adoption",
        [0.7, 0.8, 0.9, 0.95],
        "Two-way Analysis: Enforcement Cost vs. Mandate Adoption"
    )