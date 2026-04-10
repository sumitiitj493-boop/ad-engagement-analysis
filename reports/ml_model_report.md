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
- comment_length
- sentiment_polarity
- comment text (TF-IDF)

## Model Performance
### Logistic Regression
- Accuracy: 0.5621
- F1 Score: 0.2019

```text
              precision    recall  f1-score   support

           0     0.5838    0.8684    0.6983       874
           1     0.4192    0.1330    0.2019       624

    accuracy                         0.5621      1498
   macro avg     0.5015    0.5007    0.4501      1498
weighted avg     0.5153    0.5621    0.4915      1498
```

### Random Forest
- Accuracy: 0.5407
- F1 Score: 0.3410

```text
              precision    recall  f1-score   support

           0     0.5863    0.7231    0.6475       874
           1     0.4238    0.2853    0.3410       624

    accuracy                         0.5407      1498
   macro avg     0.5050    0.5042    0.4943      1498
weighted avg     0.5186    0.5407    0.5198      1498
```

## Best Model
Random Forest
**Real-world Predictive Model**. The cheat features (emoji_flag and hashtag_count) have been removed to avoid target leakage.
This gives a realistic evaluation of predicting engagement using only naturally provided text and sentiment.

## Feature Insight
By relying solely on text features and sentiment, we simulate a cold-start prediction environment.
For stronger ML validity, use an external outcome target such as CTR, conversion, or retention in a future phase.

## Saved Outputs
- reports/ml_confusion_matrix.png
- data/sample_predictions.csv