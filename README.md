# Ad Engagement Analysis

An end-to-end analytics project that scores Instagram ad interactions and ranks campaigns using a custom business metric.

## Objective
Brands need to know which campaigns drive high-quality engagement, not just raw comment volume.

This project builds an engagement scoring framework and dashboard to identify:
- top and bottom campaigns,
- interaction quality patterns,
- data quality confidence before reporting.

## Dataset Snapshot
- 7,488 interaction records
- 257 campaigns
- 77 users
- Source context: Instagram comments and behavior signals

## Engagement Scoring Logic
Each interaction receives a custom score:

$$
Engagement\ Score = 1 + (2 \times EmojiUsedFlag) + HashtagCount
$$

Where:
- Base comment contributes 1 point
- Emoji used contributes 2 points (if yes)
- Hashtag count contributes 1 point per hashtag

## Repository Structure
- data/ -> cleaned and engineered CSV files
- notebooks/ -> analysis workflow notebooks
- notebooks/01_eda.ipynb -> exploratory analysis
- notebooks/02_sentiment.ipynb -> sentiment workflow
- notebooks/03_engagement.ipynb -> feature engineering, ranking, validation
- app.py -> Streamlit dashboard
- train_predictive_model.py -> Machine Learning pipeline script
- requirements.txt -> Python dependencies
- reports/ -> final narrative outputs

## Interpreting ML Results
- **Predictive Power**: Our model predicts engagement using natural text features alone (comment length, sentiment polarity, and TF-IDF vectors).
- **Target Leakage Remediation**: Previously, the model used `emoji_used` and `hashtag_count` which allowed perfect predictions because they formulated the target variable. Now, it operates as a cold-start NLP problem to evaluate true text-based predictive capabilities.

## How To Run
1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run notebooks in order:
- notebooks/01_eda.ipynb
- notebooks/02_sentiment.ipynb
- notebooks/03_engagement.ipynb

4. Launch dashboard:

```bash
streamlit run app.py
```

5. Run predictive ML extension (classification baseline):

```bash
python train_predictive_model.py
```

## Generated Outputs
Running notebook 03 creates:
- data/ad_interactions_scored.csv
- data/campaign_performance.csv
- data/campaign_sentiment_engagement_final.csv

Running predictive ML extension creates:
- reports/ml_model_report.md
- reports/ml_confusion_matrix.png
- data/predicted_engagement_sample.csv

## Predictive ML Extension
To convert this into a stronger Machine Learning submission, this repository includes a binary classification task:
- Target: High_Engagement = 1 if engagement_score is above the median, else 0
- Features: comment length, sentiment polarity, TF-IDF text features (Target leakage from emoji/hashtag flags has been removed).
- Models: Logistic Regression and Random Forest
- Metrics: Accuracy, F1 Score, confusion matrix, classification report

## Validation Included
Notebook 03 includes validation checks for:
- required column presence,
- emoji value integrity (yes/no),
- engagement score min and max,
- exported row-count consistency.

## Current Findings
- Campaign performance spread is meaningful (score spread: 80).
- Top campaigns achieve stronger total engagement with consistent average interaction quality.
- Data quality checks pass for current engineered outputs.
- Interaction-level sentiment and engagement correlation is near zero in this dataset.
- Campaign-level sentiment-engagement correlation is weakly negative (about -0.16).

## Completion Status
- Core analytics pipeline: complete
- Validation and quality checks: complete
- Engagement and ranking insights: complete
- Sentiment-engagement merge analysis: complete
- Streamlit dashboard: complete
- Final report: available in reports/final_report.md

## Dashboard Features
- KPI cards (interaction count, average score, best campaign, campaign count)
- campaign and date filters
- ranked campaign table
- engagement distribution chart
- top-campaign comparison chart
- quality status block for fast trust checks

## Submission Checklist
- Run notebooks in order and confirm all CSV outputs are regenerated.
- Launch dashboard and verify all sections render correctly.
- Ensure final report exists at reports/final_report.md.
- Capture and save screenshots in assets/ with these recommended names:
	- assets/dashboard_kpi_overview.png
	- assets/dashboard_top_campaigns.png
	- assets/dashboard_priority_table.png
	- assets/notebook_validation_output.png
	- assets/notebook_sentiment_engagement_plot.png
- Add screenshot references in this README before final submission.
