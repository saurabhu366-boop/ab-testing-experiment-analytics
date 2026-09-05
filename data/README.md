# Data

This directory contains the dataset used for the A/B testing analysis.

## Files

- `marketing_AB.csv` — Original dataset used for the project.
- `marketing_AB_clean.csv` — Analytical dataset after removing the exported `Unnamed: 0` index column.

## Dataset

The dataset contains user-level observations from a marketing A/B testing experiment comparing:

- `ad` — Treatment group
- `psa` — Control group

The primary outcome is `converted`.

## Cleaning Decision

The original `Unnamed: 0` column was removed because it is a sequential exported index and does not represent an analytical feature.

No rows were removed based solely on extreme `total_ads` values. The exposure variable is strongly right-skewed, but the extreme observations were retained because there was no evidence that they were invalid.

## Important Limitations

The dataset does not contain revenue, campaign cost, profit, ROI, or customer-level economic information.

The original experiment's randomization mechanism and intended allocation cannot be independently verified from the available dataset.