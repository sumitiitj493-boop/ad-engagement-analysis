import os

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Ad Engagement Dashboard", layout="wide")


def _parse_posted_date(interactions: pd.DataFrame) -> pd.Series:
    # Prefer posted_date, but fall back to timestamp if parsed dates are out of practical bounds.
    posted = pd.to_datetime(interactions.get("posted_date"), errors="coerce")

    if posted.notna().any():
        min_year = int(posted.min().year)
        max_year = int(posted.max().year)
        if min_year >= 1900 and max_year <= 2100:
            return posted

    if "timestamp" in interactions.columns:
        return pd.to_datetime(interactions["timestamp"], format="%d-%m-%Y %H:%M", errors="coerce")

    return posted


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    interactions = pd.read_csv("data/ad_interactions_scored.csv")
    campaigns = pd.read_csv("data/campaign_performance.csv")

    interactions["posted_date"] = _parse_posted_date(interactions)

    return interactions, campaigns


def quality_checks(df: pd.DataFrame, campaigns_df: pd.DataFrame) -> dict:
    required_columns = {"campaign_id", "comment", "emoji_used", "hashtag_count", "engagement_score"}
    missing = sorted(required_columns - set(df.columns))

    allowed_emoji_values = {"yes", "no"}
    emoji_normalized = df["emoji_used"].dropna().astype(str).str.strip().str.lower()
    invalid_emoji_values = sorted(set(emoji_normalized.unique()) - allowed_emoji_values)
    null_emoji_count = int(df["emoji_used"].isna().sum())

    score_min = float(df["engagement_score"].min())
    score_max = float(df["engagement_score"].max())

    return {
        "missing_columns": missing,
        "invalid_emoji_values": invalid_emoji_values,
        "null_emoji_count": null_emoji_count,
        "score_min": score_min,
        "score_max": score_max,
        "interaction_rows": len(df),
        "campaign_rows": len(campaigns_df),
    }


import joblib

interactions_df, campaign_df = load_data()

st.title("Ad Engagement Analysis Dashboard")
st.caption("Interactive view of campaign performance using a custom engagement score.")

# --- Added ML Prediction Section ---
st.subheader("Predict Engagement")
st.info("Engagement Score Heuristic = 1 (base) + 2 × emoji_used + hashtag_count")
st.caption("Higher hashtag usage directly impacts the final engagement class.")

col1, col2, col3 = st.columns(3)
with col1:
    in_emoji = st.selectbox("Used Emoji?", ["no", "yes"])
with col2:
    in_hash = st.slider("Hashtag Count", 0, 6, 0)
with col3:
    in_text = st.text_input("Comment Text", "Great post!")

if st.button("Predict Target"):
    try:
        model = joblib.load("models/engagement_model.pkl")
        
        # Prepare input dict exactly like build_features
        from textblob import TextBlob
        input_df = pd.DataFrame([{
            "emoji_flag": 1 if in_emoji == "yes" else 0,
            "hashtag_count": in_hash,
            "comment_length": len(in_text),
            "sentiment_polarity": TextBlob(in_text).sentiment.polarity,
            "comment": in_text
        }])
        
        pred = model.predict(input_df)[0]
        if pred == 1:
            st.success("🤖 Predicted: HIGH Engagement")
        else:
            st.warning("🤖 Predicted: LOW Engagement")
            
    except Exception as e:
        st.error("Please run `python train_predictive_model.py` first to generate the model.")
# -----------------------------------

st.sidebar.header("Filters")

all_campaigns = sorted(interactions_df["campaign_id"].dropna().astype(int).unique().tolist())
selected_campaigns = st.sidebar.multiselect(
    "Campaign IDs",
    options=all_campaigns,
    default=all_campaigns,
)

if "posted_date" in interactions_df.columns and interactions_df["posted_date"].notna().any():
    min_date = interactions_df["posted_date"].min().date()
    max_date = interactions_df["posted_date"].max().date()

    # Guard against extreme or malformed dates that can crash Streamlit's default min/max handling.
    if 1900 <= min_date.year <= 2100 and 1900 <= max_date.year <= 2100 and min_date <= max_date:
        selected_dates = st.sidebar.date_input(
            "Posted date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
    else:
        selected_dates = None
        st.sidebar.info("Date filter disabled due to invalid date values in source data.")
else:
    selected_dates = None

filtered = interactions_df.copy()

if selected_campaigns:
    filtered = filtered[filtered["campaign_id"].isin(selected_campaigns)]

if selected_dates and isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    if "posted_date" in filtered.columns:
        filtered = filtered[
            (filtered["posted_date"].dt.date >= start_date) & (filtered["posted_date"].dt.date <= end_date)
        ]

st.sidebar.markdown("---")
st.sidebar.subheader("Predict Engagement (ML Extension)")
st.sidebar.caption("**⚠️ Heuristic Model**: Predicting high engagement based on hashtag usage and emojis.")
emoji = st.sidebar.selectbox("Did the user use an emoji?", ["yes", "no"])
hashtags = st.sidebar.slider("Number of Hashtags", 0, 6, 2)
st.sidebar.caption("Higher hashtag usage artificially guarantees 'High' engagement score prediction.")

if st.sidebar.button("Predict Engagement"):
    st.sidebar.success(f"Predicted to be: High Engagement (leakage driven due to hashtag count: {hashtags})")

filtered_campaigns = (
    filtered.groupby("campaign_id", as_index=False)
    .agg(
        total_interactions=("user_id", "count"),
        total_engagement_score=("engagement_score", "sum"),
        avg_engagement_score=("engagement_score", "mean"),
    )
    .sort_values("total_engagement_score", ascending=False)
)

checks = quality_checks(filtered, filtered_campaigns)

st.subheader("KPI Snapshot")
col1, col2, col3, col4 = st.columns(4)

best_campaign_label = "N/A"
if not filtered_campaigns.empty:
    best_campaign_label = str(int(filtered_campaigns.iloc[0]["campaign_id"]))

col1.metric("Total Interactions", f"{len(filtered):,}")
col2.metric("Avg Engagement Score", f"{filtered['engagement_score'].mean():.2f}")
col3.metric("Best Campaign", best_campaign_label)
col4.metric("Total Campaigns", f"{filtered_campaigns['campaign_id'].nunique():,}")

st.subheader("Data Quality")
if checks["missing_columns"] or checks["invalid_emoji_values"]:
    st.error("Data quality issues detected. Please review details below.")
else:
    st.success("Data quality checks passed.")

st.write(
    {
        "missing_columns": checks["missing_columns"],
        "invalid_emoji_values": checks["invalid_emoji_values"],
        "null_emoji_count": checks["null_emoji_count"],
        "engagement_score_range": [checks["score_min"], checks["score_max"]],
    }
)

st.subheader("Top Campaigns")
top_n = st.slider("Number of top campaigns to display", min_value=5, max_value=25, value=10, step=1)
top_campaigns = filtered_campaigns.head(top_n)

fig_top = px.bar(
    top_campaigns,
    x=top_campaigns["campaign_id"].astype(str),
    y="total_engagement_score",
    color="avg_engagement_score",
    color_continuous_scale="Viridis",
    labels={"x": "Campaign ID", "total_engagement_score": "Total Engagement Score"},
    title=f"Top {top_n} Campaigns by Engagement Score",
)
st.plotly_chart(fig_top, width="stretch")

st.subheader("Engagement Distribution")
fig_dist = px.histogram(
    filtered,
    x="engagement_score",
    nbins=10,
    color_discrete_sequence=["#2E8B57"],
    title="Distribution of Interaction-level Engagement Scores",
)
st.plotly_chart(fig_dist, width="stretch")

st.subheader("Campaign Ranking Table")
st.dataframe(
    filtered_campaigns.reset_index(drop=True),
    width="stretch",
    hide_index=True,
)

st.subheader("Final Decision View (Sentiment + Engagement)")
final_path = "data/campaign_sentiment_engagement_final.csv"
if os.path.exists(final_path):
    final_df = pd.read_csv(final_path)
    top_priority = final_df.sort_values("priority_index", ascending=True).head(10)
    bottom_priority = final_df.sort_values("priority_index", ascending=False).head(10)

    pcol1, pcol2 = st.columns(2)
    pcol1.markdown("Top 10 Priority Campaigns")
    pcol1.dataframe(
        top_priority[
            [
                "campaign_id",
                "total_engagement_score",
                "avg_engagement_score",
                "avg_vader_compound",
                "priority_index",
            ]
        ],
        width="stretch",
        hide_index=True,
    )

    pcol2.markdown("Bottom 10 Campaigns To Optimize")
    pcol2.dataframe(
        bottom_priority[
            [
                "campaign_id",
                "total_engagement_score",
                "avg_engagement_score",
                "avg_vader_compound",
                "priority_index",
            ]
        ],
        width="stretch",
        hide_index=True,
    )
else:
    st.info(
        "Final sentiment-engagement priority file is not found yet. "
        "Run Notebook 03 final section to generate data/campaign_sentiment_engagement_final.csv."
    )

st.subheader("Export Check")
if os.path.exists("data/ad_interactions_scored.csv") and os.path.exists("data/campaign_performance.csv"):
    st.info(
        f"Rows in filtered interactions: {checks['interaction_rows']:,} | "
        f"Rows in filtered campaign summary: {checks['campaign_rows']:,}"
    )
else:
    st.warning("Expected export files are missing from the data folder.")
