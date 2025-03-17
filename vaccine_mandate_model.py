import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class VaccineMandateModel:
    def __init__(self):
        # Default parameters
        self.params = {
            # Efficacy parameters
            "baseline_deaths": 1000,  # Deaths without vaccine
            "vaccine_efficacy": 0.9,  # % reduction in deaths for vaccinated individuals
            
            # Adoption parameters
            "voluntary_adoption": 0.6,  # % population that would voluntarily vaccinate
            "mandate_adoption": 0.9,  # % population that would vaccinate under mandate
            
            # Utility parameters
            "value_of_life": 10000000,  # Value assigned to a life saved ($10M)
            "freedom_value": 400000000,  # Value for an entire society of maintaining freedom of choice
            "enforcement_cost": 150000000, # Cost to enforce the mandate
            
            # Risk preference
            "risk_aversion": 1.0,  # 1.0 is risk-neutral, >1 is risk-averse, <1 is risk-seeking
        }
    
    def calculate_deaths(self, adoption_rate):
        """Calculate expected deaths based on vaccine adoption rate"""
        vaccinated = adoption_rate
        unvaccinated = 1 - adoption_rate
        
        # Deaths among vaccinated (reduced by efficacy)
        vaccinated_deaths = self.params["baseline_deaths"] * vaccinated * (1 - self.params["vaccine_efficacy"])
        
        # Deaths among unvaccinated (no reduction)
        unvaccinated_deaths = self.params["baseline_deaths"] * unvaccinated
        
        return vaccinated_deaths + unvaccinated_deaths
    
    def calculate_lives_saved(self, adoption_rate):
        """Calculate lives saved compared to no vaccination"""
        deaths_with_adoption = self.calculate_deaths(adoption_rate)
        deaths_without_vaccination = self.params["baseline_deaths"]
        return deaths_without_vaccination - deaths_with_adoption
    
    def calculate_freedom_utility(self, is_mandate):
        """Calculate utility related to freedom of choice"""
        if is_mandate:
            # Freedom utility loss applies to everyone under mandate
            population = 1.0  # Assuming normalized population of 1
            return -self.params["freedom_value"] * population
        return 0  # No freedom lost without mandate
    
    def calculate_enforcement_costs(self, is_mandate):
        """Calculate costs related to enforcing the mandate"""
        if is_mandate:
            return -self.params["enforcement_cost"]
        return 0
    
    def calculate_life_utility(self, is_mandate):
        """Calculate utility from lives saved"""
        if is_mandate:
            lives_saved = self.calculate_lives_saved(self.params["mandate_adoption"])
        else:
            lives_saved = self.calculate_lives_saved(self.params["voluntary_adoption"])
        
        # Apply diminishing returns to value of life as more lives are saved
        # This creates a more realistic model where early lives saved are more valuable
        # (e.g., younger, healthier individuals or those without comorbidities)
        diminishing_factor = 0.9  # Slightly diminishing returns
        effective_lives_saved = lives_saved ** diminishing_factor
        
        return effective_lives_saved * self.params["value_of_life"]
    
    def calculate_total_utility(self, is_mandate):
        """Calculate total utility considering all factors"""
        life_utility = self.calculate_life_utility(is_mandate)
        freedom_utility = self.calculate_freedom_utility(is_mandate)
        enforcement_costs = self.calculate_enforcement_costs(is_mandate)
        
        total = life_utility + freedom_utility + enforcement_costs
        
        # Apply risk adjustment
        if total >= 0:
            return total ** self.params["risk_aversion"]
        else:
            return -((-total) ** self.params["risk_aversion"])
    
    def make_decision(self):
        """Decide whether to recommend a mandate based on utility calculations"""
        utility_with_mandate = self.calculate_total_utility(True)
        utility_without_mandate = self.calculate_total_utility(False)
        
        if utility_with_mandate > utility_without_mandate:
            return True, utility_with_mandate, utility_without_mandate
        else:
            return False, utility_with_mandate, utility_without_mandate
    
    def set_parameters(self, **kwargs):
        """Update model parameters"""
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value
            else:
                print(f"Warning: Unknown parameter '{key}'")
    
    def sensitivity_analysis(self, parameter, values):
        """Perform sensitivity analysis on a single parameter"""
        results = []
        original_value = self.params[parameter]
        
        for value in values:
            self.params[parameter] = value
            decision, util_mandate, util_voluntary = self.make_decision()
            results.append({
                "value": value,
                "decision": "Mandate" if decision else "Voluntary",
                "utility_mandate": util_mandate,
                "utility_voluntary": util_voluntary,
                "utility_difference": util_mandate - util_voluntary
            })
        
        # Reset parameter to original value
        self.params[parameter] = original_value
        return pd.DataFrame(results)
    
    def two_way_analysis(self, param1, values1, param2, values2):
        """Perform two-way sensitivity analysis on two parameters"""
        results = []
        original_value1 = self.params[param1]
        original_value2 = self.params[param2]
        
        for val1 in values1:
            for val2 in values2:
                self.params[param1] = val1
                self.params[param2] = val2
                decision, _, _ = self.make_decision()
                results.append({
                    param1: val1,
                    param2: val2,
                    "decision": "Mandate" if decision else "Voluntary"
                })
        
        # Reset parameters to original values
        self.params[param1] = original_value1
        self.params[param2] = original_value2
        
        return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
    model = VaccineMandateModel()
    
    # Make a decision with default parameters
    decision, util_mandate, util_voluntary = model.make_decision()
    print(f"Decision with default parameters: {'Mandate' if decision else 'Voluntary'}")
    print(f"Utility with mandate: {util_mandate:.2f}")
    print(f"Utility without mandate: {util_voluntary:.2f}")
    print(f"Difference: {util_mandate - util_voluntary:.2f}")
    
    # Sensitivity analysis on vaccine efficacy
    efficacy_analysis = model.sensitivity_analysis(
        "vaccine_efficacy", 
        np.linspace(0.5, 0.99, 10)
    )
    print("\nSensitivity Analysis - Vaccine Efficacy:")
    print(efficacy_analysis)
    
    # Sensitivity analysis on mandate adoption
    adoption_analysis = model.sensitivity_analysis(
        "mandate_adoption",
        np.linspace(0.6, 0.99, 10)
    )
    print("\nSensitivity Analysis - Mandate Adoption:")
    print(adoption_analysis)
    
    # Two-way sensitivity analysis
    two_way = model.two_way_analysis(
        "freedom_value", np.linspace(1000, 10000, 5),
        "vaccine_efficacy", np.linspace(0.7, 0.95, 5)
    )
    print("\nTwo-way Analysis - Freedom Value vs. Vaccine Efficacy:")
    print(two_way.pivot(index="freedom_value", columns="vaccine_efficacy", values="decision"))