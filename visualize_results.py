import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaccine_mandate_model import VaccineMandateModel

def plot_sensitivity(model, parameter, values, title, xlabel):
    """Create a sensitivity analysis plot for a single parameter"""
    results = model.sensitivity_analysis(parameter, values)
    
    plt.figure(figsize=(10, 6))
    plt.plot(results['value'], results['utility_mandate'], 'b-', label='Mandate')
    plt.plot(results['value'], results['utility_voluntary'], 'r-', label='Voluntary')
    plt.axhline(y=0, color='gray', linestyle=':')
    
    # Mark the decision boundary
    decision_changes = []
    for i in range(1, len(results)):
        if results['decision'].iloc[i] != results['decision'].iloc[i-1]:
            decision_changes.append(results['value'].iloc[i])
    
    for dc in decision_changes:
        plt.axvline(x=dc, color='green', linestyle='--', alpha=0.7)
        plt.text(dc, plt.ylim()[1]*0.9, f"Decision\nBoundary\n{dc:.3f}", 
                 horizontalalignment='center', backgroundcolor='white')
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Total Utility')
    plt.legend()
    plt.grid(True, alpha=0.3)
    return plt

def plot_two_way_analysis(model, param1, values1, param2, values2, 
                          param1_label, param2_label, title):
    """Create a heatmap for two-way sensitivity analysis"""
    results = model.two_way_analysis(param1, values1, param2, values2)
    
    # Convert decision to numeric for heatmap
    pivot_data = results.pivot(index=param1, columns=param2, values="decision")
    pivot_data_numeric = pivot_data.applymap(lambda x: 1 if x == "Mandate" else 0)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_data_numeric, annot=pivot_data, fmt="", cmap="RdBu_r", 
                linewidths=.5, cbar=False)
    
    plt.title(title)
    plt.xlabel(param2_label)
    plt.ylabel(param1_label)
    return plt

if __name__ == "__main__":
    model = VaccineMandateModel()
    
    # Plot sensitivity analysis for vaccine efficacy
    efficacy_values = np.linspace(0.5, 0.99, 20)
    efficacy_plot = plot_sensitivity(
        model, 
        "vaccine_efficacy", 
        efficacy_values,
        "Impact of Vaccine Efficacy on Decision",
        "Vaccine Efficacy (proportion of deaths prevented)"
    )
    efficacy_plot.savefig("efficacy_sensitivity.png")
    
    # Plot sensitivity analysis for mandate adoption rate
    adoption_values = np.linspace(0.6, 0.99, 20)
    adoption_plot = plot_sensitivity(
        model, 
        "mandate_adoption", 
        adoption_values,
        "Impact of Mandate Adoption Rate on Decision",
        "Mandate Adoption Rate"
    )
    adoption_plot.savefig("adoption_sensitivity.png")
    
    # Plot sensitivity analysis for freedom value
    freedom_values = np.linspace(1000, 15000, 20)
    freedom_plot = plot_sensitivity(
        model, 
        "freedom_value", 
        freedom_values,
        "Impact of Freedom Value on Decision",
        "Value Placed on Freedom of Choice (per person)"
    )
    freedom_plot.savefig("freedom_sensitivity.png")
    
    # Plot two-way sensitivity
    freedom_values_2way = np.linspace(1000, 10000, 10)
    efficacy_values_2way = np.linspace(0.7, 0.95, 10)
    
    two_way_plot = plot_two_way_analysis(
        model,
        "freedom_value", freedom_values_2way,
        "vaccine_efficacy", efficacy_values_2way,
        "Freedom Value", "Vaccine Efficacy",
        "Decision Map: Freedom Value vs. Vaccine Efficacy"
    )
    two_way_plot.savefig("two_way_analysis.png")
    
    # Another two-way analysis: enforcement cost vs voluntary adoption
    enforcement_values = np.linspace(1000000, 5000000, 10)
    voluntary_values = np.linspace(0.4, 0.8, 10)
    
    enf_vol_plot = plot_two_way_analysis(
        model,
        "enforcement_cost", enforcement_values,
        "voluntary_adoption", voluntary_values,
        "Enforcement Cost ($)", "Voluntary Adoption Rate",
        "Decision Map: Enforcement Cost vs. Voluntary Adoption"
    )
    enf_vol_plot.savefig("enforcement_voluntary.png")
    
    plt.close('all')
    print("Visualizations have been saved as PNG files")