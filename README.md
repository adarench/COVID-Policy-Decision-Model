# COVID-19 Vaccine Mandate Decision Model

A utility-based decision model for evaluating whether a government should implement a COVID-19 vaccine mandate.

## Overview

This project implements a computational decision model that weighs the benefits, costs, and ethical considerations of vaccine mandates versus voluntary vaccination policies. The model allows for sensitivity analysis across multiple parameters, including:

- Vaccine efficacy
- Voluntary and mandate-driven adoption rates
- Value placed on human life
- Value placed on freedom of choice
- Costs of mandate enforcement
- Risk preferences of decision makers

## Files in this Repository

- `vaccine_mandate_model.py`: Core decision model implementing utility calculations
- `summary_tables.py`: Generates sensitivity analysis tables for various parameters
- `visualize_results.py`: Creates data visualizations of model results (requires matplotlib and seaborn)
- `writeup.md`: Comprehensive analysis of the model, key findings, and limitations

## Usage

To view sensitivity analysis results:

```bash
python summary_tables.py
```

To generate visualizations (requires seaborn):

```bash
python visualize_results.py
```

## Key Findings

1. **Mandate Adoption Rate is Critical**: If a mandate would only increase vaccination by ~10% (e.g., from 60% to 70%), voluntary policies are preferred.

2. **Diminishing Returns**: When we account for diminishing returns in the value of lives saved, the case for mandates weakens but remains positive in most scenarios.

3. **Value Tradeoffs**: The model quantifies the tradeoff between lives saved and freedom preservation, forcing explicit consideration of these competing values.

4. **Decision Thresholds**: When mandate enforcement is costly (~$150 million) and societal freedom is highly valued (~$400 million), the vaccination rate needs to reach approximately 75% under a mandate to justify its costs.

## Limitations

This model necessarily simplifies complex realities. It doesn't account for waning immunity, virus variants, or heterogeneous risk across populations. Placing explicit numerical values on freedom and human life is inherently difficult and ethically complex.