import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import datetime
from bs4 import BeautifulSoup

# Page config
st.set_page_config(page_title="AXII Artist Dashboard", layout="wide")

st.markdown("""
<style>
.big-title {
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    color: #3C3C3C;
    padding-top: 20px;
}
.metric-card {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    text-align: center;
    margin: 10px;
}
.artist-image {
    max-height: 150px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 10px;
}
.news-article {
    font-size: 14px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">AXII Artist Intelligence Dashboard</div>', unsafe_allow_html=True)

st.markdown("""
Visualizing artist value through:
- **Cultural Capital Index (CCI)**
- **Emotional Engagement Score (EES)**
- **Repeat Sales Market Index (RSMI)**
""")

# Function to fetch news data from NewsAPI.org
def fetch_news_mentions(artist_name, api_key):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q=\"{artist_name}\"&from={datetime.date.today().isoformat()}&sortBy=relevancy&pageSize=5&apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        articles = results.get("articles", [])
        score = min(len(articles) * 10, 100)
        return score, articles
    except:
        return 50, []

# Simulate Instagram engagement score
def simulate_instagram_engagement(artist_name):
    return hash(artist_name) % 30 + 60

# Scrape auction sales from Phillips
def fetch_auction_sales_score(artist_name):
    try:
        query = artist_name.replace(" ", "+")
        url = f"https://www.phillips.com/search?search={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results_text = soup.find('span', class_='search-results-count')
        if results_text:
            count = int(''.join(filter(str.isdigit, results_text.text)))
            score = min(count // 5, 100)
        else:
            score = 50
    except:
        score = 50
    return score

# Sample data with image URLs (add your own or fetch dynamically)
data = {
    "Artist": ["Tschabalala Self", "Jordan Casteel", "Cao Fei"],
    "Image": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Tschabalala_Self_2021.jpg/400px-Tschabalala_Self_2021.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Jordan_Casteel_2020.jpg/400px-Jordan_Casteel_2020.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Cao_Fei%2C_2019.jpg/400px-Cao_Fei%2C_2019.jpg"
    ],
    "Cultural Capital Index (CCI)": [82, 77, 90],
    "Emotional Engagement Score (EES)": [88, 91, 86],
    "Repeat Sales Market Index (RSMI)": [65, 70, 68],
    "News": [[], [], []]
}

# DataFrame
df = pd.DataFrame(data)

# Sidebar input
st.sidebar.header("Add New Artist")
new_artist = st.sidebar.text_input("Artist Name")
api_key = st.sidebar.text_input("NewsAPI Key", type="password")

if st.sidebar.button("Fetch & Add Artist"):
    if new_artist and api_key:
        cci_score, articles = fetch_news_mentions(new_artist, api_key)
        ees_score = simulate_instagram_engagement(new_artist)
        rsmi_score = fetch_auction_sales_score(new_artist)

        new_data = {
            "Artist": new_artist,
            "Image": "https://via.placeholder.com/300x150.png?text=Artist+Image",
            "Cultural Capital Index (CCI)": cci_score,
            "Emotional Engagement Score (EES)": ees_score,
            "Repeat Sales Market Index (RSMI)": rsmi_score,
            "News": [articles]
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

# Artist selection
artists_selected = st.multiselect("Select artists to compare:", df["Artist"].tolist(), default=df["Artist"].tolist())
filtered_df = df[df["Artist"].isin(artists_selected)]

# Index breakdown (cards style)
st.markdown("### Artist Scores")
cols = st.columns(len(filtered_df))
for idx, row in filtered_df.iterrows():
    with cols[list(filtered_df.index).index(idx)]:
        st.markdown(f"""
        <div class="metric-card">
            <img src="{row['Image']}" class="artist-image" />
            <h3>{row['Artist']}</h3>
            <p><b>CCI:</b> {row['Cultural Capital Index (CCI)']}</p>
            <p><b>EES:</b> {row['Emotional Engagement Score (EES)']}</p>
            <p><b>RSMI:</b> {row['Repeat Sales Market Index (RSMI)']}</p>
        </div>
        """, unsafe_allow_html=True)

# Show News Articles
st.markdown("### Recent News Highlights")
for idx, row in filtered_df.iterrows():
    st.subheader(row["Artist"])
    news_list = row.get("News", [])
    if isinstance(news_list, list):
        for article in news_list:
            st.markdown(f"<div class='news-article'>🔹 <a href='{article['url']}' target='_blank'>{article['title']}</a></div>", unsafe_allow_html=True)
    else:
        st.write("No articles available.")

# Radar chart
melted = filtered_df.melt(id_vars=["Artist"], value_vars=["Cultural Capital Index (CCI)", "Emotional Engagement Score (EES)", "Repeat Sales Market Index (RSMI)"], var_name="Index", value_name="Score")
fig = px.line_polar(
    melted,
    r="Score",
    theta="Index",
    color="Artist",
    line_close=True,
    title="AXII Index Radar"
)
fig.update_traces(fill='toself')
st.plotly_chart(fig, use_container_width=True)

# Table
st.subheader("Raw AXII Data")
st.dataframe(filtered_df.set_index("Artist"))
