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
- requirements.txt -> Python dependencies
- reports/ -> final narrative outputs

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

## Generated Outputs
Running notebook 03 creates:
- data/ad_interactions_scored.csv
- data/campaign_performance.csv

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

## Dashboard Features
- KPI cards (interaction count, average score, best campaign, campaign count)
- campaign and date filters
- ranked campaign table
- engagement distribution chart
- top-campaign comparison chart
- quality status block for fast trust checks
