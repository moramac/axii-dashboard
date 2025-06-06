import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import datetime
from bs4 import BeautifulSoup

# Page config
st.set_page_config(page_title="AXII Artist Dashboard", layout="centered")

st.title("AXII Artist Intelligence Dashboard")
st.markdown("Visualizing artist value through Cultural Capital, Emotional Engagement, and Market Indices.")

# Function to fetch news count from NewsAPI.org
def fetch_news_mentions(artist_name, api_key):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q=\"{artist_name}\"&from={datetime.date.today().isoformat()}&sortBy=relevancy&apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        total = results.get("totalResults", 0)
        score = min(total // 2, 100)  # Normalize to 0–100 scale
    except:
        score = 50
    return score

# Function to simulate Instagram engagement score
def simulate_instagram_engagement(artist_name):
    return hash(artist_name) % 30 + 60  # Mock score between 60 and 90

# Function to scrape auction sales data (Phillips example)
def fetch_auction_sales_score(artist_name):
    try:
        query = artist_name.replace(" ", "+")
        url = f"https://www.phillips.com/search?search={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract estimated number of auction results for artist (simplified logic)
        results_text = soup.find('span', class_='search-results-count')
        if results_text:
            count = int(''.join(filter(str.isdigit, results_text.text)))
            score = min(count // 5, 100)  # Normalize to 0–100 scale
        else:
            score = 50
    except:
        score = 50
    return score

# Initial AXII data for a few artists
data = {
    "Artist": ["Tschabalala Self", "Jordan Casteel", "Cao Fei"],
    "Cultural Capital Index (CCI)": [82, 77, 90],
    "Emotional Engagement Score (EES)": [88, 91, 86],
    "Repeat Sales Market Index (RSMI)": [65, 70, 68]
}

# DataFrame
df = pd.DataFrame(data)

# User input for new artist
st.sidebar.header("Add New Artist")
new_artist = st.sidebar.text_input("Artist Name")
api_key = st.sidebar.text_input("NewsAPI Key", type="password")

if st.sidebar.button("Fetch & Add Artist"):
    if new_artist and api_key:
        cci_score = fetch_news_mentions(new_artist, api_key)
        ees_score = simulate_instagram_engagement(new_artist)
        rsmi_score = fetch_auction_sales_score(new_artist)

        new_data = {
            "Artist": new_artist,
            "Cultural Capital Index (CCI)": cci_score,
            "Emotional Engagement Score (EES)": ees_score,
            "Repeat Sales Market Index (RSMI)": rsmi_score
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

# Select artist(s)
artists_selected = st.multiselect("Select artists to compare:", df["Artist"].tolist(), default=df["Artist"].tolist())

# Filter data
filtered_df = df[df["Artist"].isin(artists_selected)]

# Melt data for radar chart
melted = filtered_df.melt(id_vars=["Artist"], var_name="Index", value_name="Score")

# Radar chart
fig = px.line_polar(
    melted,
    r="Score",
    theta="Index",
    color="Artist",
    line_close=True,
    title="AXII Index Comparison"
)
fig.update_traces(fill='toself')

st.plotly_chart(fig)

# Display table
st.subheader("Raw AXII Data")
st.dataframe(filtered_df.set_index("Artist"))
