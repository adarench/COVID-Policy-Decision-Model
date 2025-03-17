# COVID-19 Vaccine Mandate Decision Model

## Model Overview

I've developed a decision model that evaluates whether a government should implement a COVID-19 vaccine mandate based on various parameters related to vaccine efficacy, adoption rates, and societal values. The model uses a utility-based approach where the overall utility of mandate vs. voluntary policies is calculated and compared.

### Key Components of the Decision-Making Model

1. **States**:
   - Population vaccination status (vaccinated vs. unvaccinated)
   - Baseline death rate without vaccines

2. **Actions**:
   - Implement vaccine mandate
   - Allow voluntary vaccination

3. **Outcomes**:
   - Deaths avoided through vaccination
   - Freedom of choice maintained or restricted
   - Costs of mandate enforcement

4. **Beliefs**:
   - Vaccine efficacy in preventing deaths
   - Expected adoption rates (voluntary vs. with mandate)

5. **Utilities**:
   - Value of human life (with diminishing returns)
   - Value of freedom of choice for society
   - Cost of enforcing mandate
   - Risk preference (aversion or seeking)

### Mathematical Framework

The model's decision is based on comparing total utility under mandate vs. voluntary scenarios:

**Deaths calculation**:
- Deaths among vaccinated: `baseline_deaths × adoption_rate × (1 - vaccine_efficacy)`
- Deaths among unvaccinated: `baseline_deaths × (1 - adoption_rate)`
- Total deaths: sum of the above

**Utility components**:
1. **Life utility**: `(lives_saved^diminishing_factor) × value_of_life` 
2. **Freedom utility**: `-freedom_value` (only under mandate)
3. **Enforcement costs**: `-enforcement_cost` (only under mandate)

**Total utility**: Sum of components, adjusted for risk preference:
- If utility ≥ 0: `utility^risk_aversion`
- If utility < 0: `-((-utility)^risk_aversion)`

**Decision rule**: Choose the action with higher total utility.

## Decision Tables and Sensitivity Analysis

### Baseline Decision

With our default parameters, the model recommends a mandate:

| Parameter | Value |
|-----------|-------|
| Baseline deaths | 1,000 |
| Vaccine efficacy | 90% |
| Voluntary adoption | 60% |
| Mandate adoption | 90% |
| Value of life | $10 million |
| Freedom value (society) | $400 million |
| Enforcement cost | $150 million |
| Risk aversion | 1.0 (risk-neutral) |

| Policy | Total Utility |
|--------|--------------|
| Mandate | $3.60 billion |
| Voluntary | $2.88 billion |
| Difference | $717.65 million |

### Sensitivity to Vaccine Efficacy

| Vaccine Efficacy | Decision | Utility Difference |
|------------------|----------|-------------------|
| 50% | Mandate | $196.88 million |
| 59% | Mandate | $316.86 million |
| 68% | Mandate | $435.00 million |
| 77% | Mandate | $551.59 million |
| 86% | Mandate | $666.83 million |
| 95% | Mandate | $780.86 million |

The mandate remains recommended across all reasonable efficacy values, though the advantage becomes smaller as efficacy decreases.

### Sensitivity to Freedom Value

| Freedom Value | Decision | Utility Difference |
|---------------|----------|-------------------|
| $100 million | Mandate | $1.02 billion |
| $200 million | Mandate | $917.65 million |
| $300 million | Mandate | $817.65 million |
| $400 million | Mandate | $717.65 million |
| $500 million | Mandate | $617.65 million |

Even with high societal freedom values, the mandate remains recommended given our other parameter values.

### Sensitivity to Adoption Rate

| Mandate Adoption Rate | Decision | Utility Difference |
|-----------------------|----------|-------------------|
| 65% | Voluntary | -$334.99 million |
| 72.5% | Voluntary | -$15.53 million |
| 80% | Mandate | $300.64 million |
| 87.5% | Mandate | $613.85 million |
| 95% | Mandate | $924.39 million |

There's a critical threshold around 72-75% mandate adoption rate where the decision flips from voluntary to mandate.

### Two-Way Analysis: Enforcement Cost vs. Mandate Adoption Rate

|                  | 70% Adoption | 80% Adoption | 90% Adoption | 95% Adoption |
|------------------|--------------|--------------|--------------|--------------|
| $50 million cost | Voluntary    | Mandate      | Mandate      | Mandate      |
| $100 million cost| Voluntary    | Mandate      | Mandate      | Mandate      |
| $150 million cost| Voluntary    | Mandate      | Mandate      | Mandate      |
| $200 million cost| Voluntary    | Mandate      | Mandate      | Mandate      |

This shows that low mandate adoption rates (70%) favor voluntary policies regardless of enforcement costs, while higher adoption rates favor mandates.

## Key Insights

1. **Mandate Adoption Rate is Critical**: The model is highly sensitive to the expected increase in vaccination rates from a mandate. If a mandate would only increase vaccination by ~10% (e.g., from 60% to 70%), voluntary policies are preferred.

2. **Diminishing Returns**: When we account for diminishing returns in the value of lives saved (e.g., because early vaccine adopters may be higher-risk individuals), the case for mandates weakens but remains positive in most scenarios.

3. **Value Tradeoffs**: The model quantifies the tradeoff between lives saved and freedom preservation, forcing explicit consideration of these competing values.

4. **Decision Thresholds**: When mandate enforcement is costly (~$150 million) and societal freedom is highly valued (~$400 million), the mandate adoption rate needs to reach approximately 75% to justify a mandate.

## Challenges and Limitations

1. **Simplifications**: The model necessarily simplifies complex realities. It doesn't account for waning immunity, virus variants, or heterogeneous risk across populations.

2. **Value Quantification**: Placing explicit numerical values on freedom and human life is inherently difficult and ethically complex.

3. **Distribution Effects**: The model considers aggregate utility but not distributional effects. Mandates may disproportionately impact certain groups.

4. **Implementation Realities**: The model assumes perfect implementation and enforcement, which is rarely achievable in practice.

This simplified approach nonetheless offers a structured framework for making difficult public health policy decisions while explicitly accounting for both health outcomes and societal values.