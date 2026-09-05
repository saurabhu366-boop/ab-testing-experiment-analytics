# Marketing A/B Testing & Conversion Experiment Analytics

> **Can an advertising treatment outperform a PSA—and is the observed lift large enough to justify rollout?**

An end-to-end A/B testing project analyzing a **588K-user marketing experiment** comparing an **Ad treatment** against a **PSA control**.

Rather than stopping at conversion-rate comparison, the project evaluates the experiment through a complete analytical workflow: **data quality → experiment validation → statistical inference → confidence intervals → effect size → multiple-testing correction → segment analysis → business decision**.

---

## Decision at a Glance

### **Recommendation: SHIP — Conditional on Economic Validation**

The Ad variant produced a higher observed conversion rate than the PSA control.

| Metric | Result |
|---|---:|
| Ad conversion rate | **2.5547%** |
| PSA conversion rate | **1.7854%** |
| Absolute lift | **+0.7692 percentage points** |
| Relative lift | **+43.09%** |
| 95% CI for lift | **+0.5951 to +0.9434 pp** |
| Two-proportion z-test | **p = 1.71 × 10⁻¹³** |
| Cohen's h | **0.0530 — Small** |
| Analytical practical threshold | **+0.50 pp** |
| Final decision | **SHIP** |

The observed lift is statistically significant and exceeds the project's predefined analytical threshold.

However, the recommendation is **conditional**: the dataset does not contain revenue, campaign cost, profit, or ROI data, and the experiment's original randomization process cannot be independently verified.

---

## Key Findings

### 1. The Ad group converted at a higher rate

| Group | Users | Conversions | Conversion Rate |
|---|---:|---:|---:|
| **Ad** | 564,577 | 14,423 | **2.5547%** |
| **PSA** | 23,524 | 420 | **1.7854%** |

The observed difference was:

**+0.7692 percentage points**

with a 95% confidence interval of:

**+0.5951 to +0.9434 percentage points**

The two-proportion z-test produced:

**p = 1.71 × 10⁻¹³**

---

### 2. Statistical significance ≠ large effect

The conversion difference is highly statistically significant, but the standardized effect is small:

**Cohen's h = 0.0530**

This is an important distinction because the experiment contains more than half a million observations. With a sample this large, relatively small differences can produce extremely small p-values.

The project therefore evaluates **both statistical significance and practical significance**.

---

### 3. The observed lift exceeds the analytical practical threshold

A **+0.50 percentage-point** absolute conversion improvement was defined as an analytical threshold.

Observed:

**+0.7692 percentage points**

Therefore, the observed effect exceeds the threshold.

> **Important:** +0.50 pp is an analytical assumption, not a business-derived ROI threshold. A production decision should replace it with a threshold based on campaign economics.

---

### 4. Ad exposure differed statistically, but the effect was negligible

`total_ads` was strongly right-skewed, so a Mann–Whitney U test was used instead of relying on normality assumptions.

| Metric | Ad | PSA |
|---|---:|---:|
| Mean | 24.82 | 24.76 |
| Median | 13 | 12 |
| Q1 | 4 | 4 |
| Q3 | 27 | 26 |

Result:

- Mann–Whitney U = **6,808,288,222**
- p = **4.69 × 10⁻¹¹**
- Rank-biserial correlation = **0.0253**

Although statistically significant, the effect size is extremely small.

This reinforces the principle that **p-values should not be interpreted without effect sizes**.

---

### 5. Day-level effects were broadly positive, but not uniform

The Ad group had a positive observed conversion difference on every day.

After Benjamini–Hochberg correction for multiple comparisons, five of seven days remained statistically significant:

| Day | Ad − PSA |
|---|---:|
| Monday | **+1.07 pp** |
| Tuesday | **+1.60 pp** |
| Wednesday | **+0.96 pp** |
| Friday | **+0.62 pp** |
| Saturday | **+0.73 pp** |

Thursday and Sunday did not remain statistically significant after correction.

Tuesday had the largest observed day-level difference, but segment findings are treated as **exploratory rather than definitive targeting recommendations**.

---

### 6. Hour-level results were much less conclusive

Twenty-four hourly comparisons were tested.

After Benjamini–Hochberg correction, only **14:00** remained statistically significant:

| Metric | 14:00 |
|---|---:|
| Ad users | 43,779 |
| PSA users | 1,869 |
| Absolute difference | **+1.252 pp** |
| 95% CI | **+0.662 to +1.843 pp** |
| Adjusted p-value | **0.03179** |
| Cohen's h | **0.0856 — Small** |

Several early-hour segments had very small PSA sample sizes and zero conversions. Their apparent relative lifts are therefore unstable and were not used as targeting recommendations.

---

# Why This Analysis Is More Than a Conversion-Rate Comparison

The project deliberately follows an experiment-analysis lifecycle instead of treating the p-value as the final answer.

```text
Raw Data
    ↓
Data Profiling
    ↓
Data Cleaning
    ↓
Experiment Validation
    ↓
Statistical Inference
    ↓
Confidence Interval
    ↓
Effect Size
    ↓
Segment Analysis
    ↓
Multiple-Testing Correction
    ↓
Business Impact
    ↓
Decision