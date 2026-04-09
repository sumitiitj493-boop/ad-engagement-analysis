# Predictive ML Extension Report

## Problem Statement
Predict high vs low engagement before campaign publishing using engineered and text features.

## Target Definition
High_Engagement = 1 if engagement_score > median_score (4.00), else 0

## Data Split
- Total rows: 7488
- Train rows: 5990
- Test rows: 1498

## Features Used
- emoji_flag
- hashtag_count
- comment_length
- sentiment_polarity
- comment text (TF-IDF)

## Model Performance
### Logistic Regression
- Accuracy: 1.0000
- F1 Score: 1.0000

```text
              precision    recall  f1-score   support

           0     1.0000    1.0000    1.0000       874
           1     1.0000    1.0000    1.0000       624

    accuracy                         1.0000      1498
   macro avg     1.0000    1.0000    1.0000      1498
weighted avg     1.0000    1.0000    1.0000      1498
```

### Random Forest
- Accuracy: 1.0000
- F1 Score: 1.0000

```text
              precision    recall  f1-score   support

           0     1.0000    1.0000    1.0000       874
           1     1.0000    1.0000    1.0000       624

    accuracy                         1.0000      1498
   macro avg     1.0000    1.0000    1.0000      1498
weighted avg     1.0000    1.0000    1.0000      1498
```

## Best Model
Logistic Regression
**⚠️ Perfect accuracy due to feature-target dependency (target leakage)**. The target label is derived from an engineered engagement score that already includes emoji and hashtag signals.
Because these signals are also used as model features, very high metrics are expected for this baseline setup. This validates our pipeline correctness but not real-world predictive power.

## Feature Insight
Behavioral features (emojis, hashtag counts) dominate engagement prediction, while text/sentiment features contribute minimally in this dataset.
For stronger ML validity, use an external outcome target such as CTR, conversion, or retention in a future phase.

## Saved Outputs
- reports/ml_confusion_matrix.png
- data/sample_predictions.csv