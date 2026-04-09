# Ad Engagement Intelligence System

## Final Analytical Report

**Note on Metric:** The Engagement Score developed here is a heuristic (business-defined metric) based on assumed weights:
`Engagement Score = 1 + 2×emoji + hashtag_count`
It is not learned from data but used as a proxy for engagement quality to rank campaigns.

## Project Pipeline
1. `cleaned.csv` → Raw comment data
2. Feature engineering
3. `ad_interactions_scored.csv`
4. Campaign aggregation
5. `campaign_performance.csv`
6. Sentiment integration
7. Final ranking
8. ML prediction
9. Dashboard visualization

## 9. Predictive Modeling Extension

A supervised machine learning model was developed to predict high vs low engagement.

- **Target:** `High_Engagement = 1` if `engagement_score > median`
- **Features:** Emoji usage, hashtag count, comment length, sentiment polarity, TF-IDF text
- **Models:** Logistic Regression, Random Forest
- **Key Result:** Perfect accuracy observed due to feature-target dependency (target leakage).
- **Interpretation:** Model validates pipeline correctness but not real-world predictive power. Behavioral features dominate engagement prediction.
- **Future Work:** Use CTR, conversions, or retention as independent targets.
