import os

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Ad Engagement Dashboard", layout="wide")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    interactions = pd.read_csv("data/ad_interactions_scored.csv")
    campaigns = pd.read_csv("data/campaign_performance.csv")

    if "posted_date" in interactions.columns:
        interactions["posted_date"] = pd.to_datetime(interactions["posted_date"], errors="coerce")

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


interactions_df, campaign_df = load_data()

st.title("Ad Engagement Analysis Dashboard")
st.caption("Interactive view of campaign performance using a custom engagement score.")

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
    selected_dates = st.sidebar.date_input("Posted date range", value=(min_date, max_date))
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
st.plotly_chart(fig_top, use_container_width=True)

st.subheader("Engagement Distribution")
fig_dist = px.histogram(
    filtered,
    x="engagement_score",
    nbins=10,
    color_discrete_sequence=["#2E8B57"],
    title="Distribution of Interaction-level Engagement Scores",
)
st.plotly_chart(fig_dist, use_container_width=True)

st.subheader("Campaign Ranking Table")
st.dataframe(
    filtered_campaigns.reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Export Check")
if os.path.exists("data/ad_interactions_scored.csv") and os.path.exists("data/campaign_performance.csv"):
    st.info(
        f"Rows in filtered interactions: {checks['interaction_rows']:,} | "
        f"Rows in filtered campaign summary: {checks['campaign_rows']:,}"
    )
else:
    st.warning("Expected export files are missing from the data folder.")
