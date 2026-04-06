import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Social Media Behavior Analysis", layout="wide")

st.title("Social Media User Behavior Analysis")
st.markdown("Analyzing how users interact through comments on Instagram.")

# TODO: Add data loading logic here
# @st.cache_data
# def load_data():
#     return pd.read_csv("data/comments_cleaned.csv")
# df = load_data()

st.sidebar.header("Navigation")
sections = ["Overview", "User Engagement", "Content Behavior", "Photo Engagement", "Sentiment Analysis"]
selection = st.sidebar.radio("Go to", sections)

if selection == "Overview":
    st.header("Project Overview")
    st.write("This dashboard explores Instagram commenting behavior, analyzing structural patterns, emoji/hashtag usage, and sentiment.")
    st.info("Please place `comments_cleaned.csv` into the `data/` directory to begin analysis.")
