# Assumptions

## Experiment Assumptions

### Randomization

The analysis assumes that users were assigned to the Ad and PSA groups through an appropriate experimental assignment process.

The dataset does not provide enough information to independently verify the randomization mechanism.

Therefore, causal interpretation is conditional on proper randomization.

---

## Sample Allocation

The observed experiment allocation is approximately:

- Ad: 96%
- PSA: 4%

The SRM analysis evaluates the observed allocation against an assumed 96% / 4% allocation.

This allocation is inferred from the experimental dataset structure and cannot be independently confirmed as the original intended allocation.

---

## Independence

The analysis assumes that each user represents an independent experimental observation.

A duplicate-user check found no duplicate user IDs in the analytical dataset.

---

## Conversion Metric

`converted` is treated as a binary outcome:

- True = converted
- False = did not convert

No weighting or imputation is applied.

---

## Exposure Variable

`total_ads` is treated as an observed exposure/engagement variable.

Extreme values are retained because no evidence was found that they were invalid.

Because exposure is not an independently randomized treatment variable, differences in `total_ads` are not interpreted as causal treatment effects.

---

## Practical Significance Threshold

A +0.50 percentage-point absolute conversion improvement is used as the practical significance threshold.

This is an analytical assumption rather than a business-derived threshold.

A production decision should replace this threshold with one based on actual:

- Incremental revenue
- Advertising cost
- Profit margin
- Customer value
- Opportunity cost

---

## Segment Analysis

Day and hour are treated as exploratory behavioral/exposure segments.

They are not assumed to be pre-treatment characteristics.

Therefore, segment-level differences should not automatically be interpreted as causal treatment-effect heterogeneity.

---

## Multiple Comparisons

Benjamini–Hochberg correction is used to control the false discovery rate across exploratory segment comparisons.

Raw p-values are retained for transparency, but adjusted p-values determine whether segment-level results remain statistically significant.

---

## Business Impact

The dataset does not contain:

- Revenue
- Average order value
- Advertising spend
- Campaign cost
- Profit
- Customer lifetime value

Therefore, actual financial ROI cannot be calculated.

Illustrative conversion scenarios use assumed audience sizes and observed conversion rates and must not be presented as observed revenue or profit.

---

## Causal Interpretation

The primary Ad-versus-PSA comparison is interpreted as experimental evidence under the assumption of proper randomization.

Because the randomization mechanism cannot be independently verified, conclusions use conditional language where appropriate.

The project does not claim that the dataset alone proves a causal effect.