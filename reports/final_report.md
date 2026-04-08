# Final Project Report: Ad Engagement Analysis

## 1. Executive Summary
This project analyzed Instagram ad interaction data to rank campaigns using a custom engagement score and assess whether sentiment adds predictive value to campaign performance.

The final result is a validated analytics pipeline, dashboard, and decision-ready campaign priority output.

## 2. Dataset Summary
- Total interactions: 7,488
- Total campaigns: 257
- Unique users: 77

## 3. Engagement Metric
The project uses a business-weighted interaction score:

Engagement Score = 1 + (2 x EmojiUsedFlag) + HashtagCount

Interpretation:
- Base comment effort: +1
- Emotional signal (emoji): +2
- Amplification intent (hashtags): +1 each

## 4. Validation Outcomes
Quality checks passed on engineered outputs:
- Required columns present
- Emoji value integrity verified (yes/no)
- Score range sanity confirmed
- Export row counts matched expected in-memory counts

## 5. Campaign Performance Findings
- Score spread across campaigns is substantial (80 points), indicating clear separation between stronger and weaker campaigns.
- Top campaigns show consistently strong total and average engagement.
- Bottom-priority campaigns can be targeted for creative or audience optimization.

## 6. Sentiment + Engagement Findings
Two sentiment approaches were tested (TextBlob and VADER).

Observed behavior:
- Most comments are neutral or near-neutral in lexical polarity.
- Interaction-level correlation between sentiment and engagement is near zero.
- Campaign-level correlation between average sentiment and total engagement is weakly negative (~ -0.16).

Business implication:
- In this dataset, engagement appears to be driven more by interaction behavior patterns (emoji/hashtags/volume) than textual sentiment.

## 7. Final Deliverables
- Cleaned and scored datasets in data/
- Notebook analysis workflow in notebooks/
- Interactive dashboard in app.py
- Documentation in README.md
- This final report in reports/final_report.md

## 8. Recommended Next Actions
1. A/B test creative variants on campaigns in the bottom-priority set.
2. Segment high-performing campaigns by content type and posting pattern.
3. Expand sentiment signals using domain-specific lexicons or emoji-aware sentiment models.
4. Add time-based trend tracking in dashboard for weekly campaign monitoring.
