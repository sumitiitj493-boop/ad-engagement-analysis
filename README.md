# Ad Engagement Analysis

## Overview
An end-to-end data analysis project measuring the effectiveness of 
257 Instagram ad campaigns through 7,488 user interactions. 
This project identifies top-performing campaigns, user engagement 
patterns, and sentiment towards sponsored content.

## Business Problem
Brands invest heavily in Instagram ad campaigns but struggle to 
measure which campaigns actually drive engagement and which fall flat.
This project builds an analytical framework to answer that question
using real interaction data.

## Key Questions
- Which ad campaigns generated the highest user engagement?
- Are users emotionally responding to ads? (emoji as engagement signal)
- Are users amplifying ads further? (hashtag count as sharing intent)
- What is the sentiment towards sponsored posts — positive or negative?
- Who are the power engagers — potential brand advocates?
- What makes a high-performing ad campaign vs a low-performing one?

## Tech Stack
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Analysis-green)
![NLP](https://img.shields.io/badge/NLP-VADER%20%7C%20TextBlob-purple)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

## Project Structure
data/                  → Raw campaign interaction dataset  
notebooks/             → Step-by-step analysis notebooks  
  01_eda.ipynb         → Campaign & user exploration  
  02_sentiment.ipynb   → Sentiment analysis of ad comments  
  03_engagement.ipynb  → Engagement scoring & campaign ranking  
assets/                → Charts and dashboard screenshots  
reports/               → Final insights summary  
app.py                 → Interactive Streamlit dashboard  
requirements.txt       → All dependencies  

## Dataset
7,488 user interactions · 257 ad campaigns · 77 unique users  
Platform: Instagram · Period: April 2023

## Key Findings
*(Updated as analysis progresses)*

## Live Dashboard
*(Streamlit deployment link — added Day 5)*
