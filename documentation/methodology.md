# Methodology

## 1. Objective

The objective of this analysis is to determine whether the Ad treatment produces a meaningful improvement in user conversion compared with the PSA control.

The analysis follows the lifecycle:

Raw Data → Data Quality → Experiment Validation → Statistical Inference → Effect Size → Segment Analysis → Multiple-Testing Correction → Business Impact → Decision

---

## 2. Primary Metric

The primary outcome metric is conversion rate:

Conversion Rate = Conversions / Users

The primary comparison is:

Ad conversion rate − PSA conversion rate

A positive value indicates higher conversion in the Ad group.

---

## 3. Hypothesis Testing

### Null Hypothesis

H₀: The conversion rates of Ad and PSA are equal.

### Alternative Hypothesis

H₁: The conversion rates differ.

A two-sided test is used because the initial objective is to determine whether the treatment produces a statistically different conversion rate rather than assuming the direction in advance.

Significance level:

α = 0.05

Confidence level:

95%

---

## 4. Two-Proportion Z-Test

A two-proportion z-test is used to compare conversion rates between the two experiment groups.

The test evaluates whether the observed difference in proportions is larger than would reasonably be expected from sampling variation.

The analysis reports:

- Z-statistic
- p-value
- Absolute conversion difference
- 95% confidence interval

---

## 5. Confidence Interval

The 95% confidence interval is calculated for:

Ad conversion rate − PSA conversion rate

The interval provides a range of plausible values for the population-level difference under the assumptions of the statistical model.

If the interval excludes zero, the data provide evidence of a difference between the groups at the corresponding confidence level.

---

## 6. Effect Size

Statistical significance alone does not indicate whether an effect is practically meaningful.

Cohen's h is used to quantify the standardized difference between two proportions.

The analysis reports Cohen's h alongside the p-value and confidence interval.

Interpretation:

- |h| < 0.20 → small effect
- |h| ≈ 0.50 → medium effect
- |h| ≈ 0.80 → large effect

---

## 7. Practical Significance

A practical significance threshold of +0.50 percentage points was defined for this project.

This threshold is an analytical assumption because the dataset does not contain sufficient business information to derive an economic threshold.

The threshold is therefore used as a decision framework rather than as a claim about the organization's actual economics.

---

## 8. Exposure Analysis

The `total_ads` variable is strongly right-skewed.

Because the distribution does not support relying on normality assumptions, the Mann–Whitney U test is used to compare the exposure distributions between Ad and PSA.

The analysis reports:

- Median
- IQR
- Mann–Whitney U statistic
- p-value
- Rank-biserial correlation

Rank-biserial correlation is used as the effect-size measure.

The exposure analysis is treated as a secondary analysis and is not interpreted as evidence that treatment assignment caused greater exposure.

---

## 9. Experiment Validation

Before interpreting the treatment effect, structural checks are performed:

- Duplicate users
- Missing conversion values
- Treatment/control integrity
- Category validity
- Sample Ratio Mismatch
- Exposure-value integrity

The observed 96% Ad / 4% PSA allocation is evaluated against the assumed allocation using a chi-square goodness-of-fit test.

Because the intended allocation cannot be independently verified from the dataset, passing the SRM check does not prove that the experiment was randomized correctly.

---

## 10. Segment Analysis

Exploratory analysis is performed across:

- Day of week
- Hour of day

For each segment, the analysis calculates:

- Ad conversion rate
- PSA conversion rate
- Absolute difference
- Relative lift
- Statistical significance
- 95% confidence interval
- Cohen's h

---

## 11. Multiple-Testing Correction

Testing multiple segments increases the probability of obtaining statistically significant results by chance.

Benjamini–Hochberg false-discovery-rate correction is therefore applied separately to:

- 7 day-level comparisons
- 24 hour-level comparisons

Segment findings are interpreted using the adjusted p-values rather than the raw p-values alone.

---

## 12. Decision Framework

The final decision uses the following criteria.

### SHIP

Consider shipping when:

- The primary result is statistically significant.
- The confidence interval supports a positive effect.
- The observed effect exceeds the predefined practical threshold.
- No major experiment-validity problems are detected.
- Business economics support the additional conversions.

### DO NOT SHIP

Consider not shipping when:

- The treatment produces a negative or negligible effect.
- The observed effect does not meet the practical threshold.
- Major validity problems undermine confidence in the result.

### NEED MORE DATA

Consider collecting additional evidence when:

- The result is statistically inconclusive.
- The confidence interval includes effects that could be practically meaningful.
- The experiment lacks sufficient precision for the business decision.

---

## 13. Business Translation

The dataset does not contain revenue, cost, margin, or profit information.

Therefore, the analysis does not claim incremental revenue or ROI.

Instead, the observed conversion difference is translated into an illustrative number of incremental conversions for a hypothetical eligible audience.

Any such scenario is explicitly labeled as illustrative rather than observed business performance.