import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import datetime

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
.artist-image, .sidebar-artist-image {
    max-height: 150px;
    max-width: 150px;
    object-fit: contain;
    border-radius: 10px;
    margin-bottom: 10px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}
.news-article {
    font-size: 14px;
    margin: 5px 0;
}
.sidebar-artist {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.sidebar-artist img {
    margin-right: 10px;
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

def fetch_trending_artnet():
    url = "https://www.artnet.com/artists/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Artnet trending artists are inside elements like <a> under trending sections, but the exact selector may vary:
        # Example selector (adjust if needed):
        anchors = soup.select("div.TrendingArtistsList a")  # adjust selector if website changes
        artists = []
        for a in anchors:
            name = a.get_text(strip=True)
            if name and name not in artists:
                artists.append(name)
        return artists[:10]
    except Exception as e:
        st.error(f"Failed to fetch trending artists from Artnet: {e}")
        return []

# Wikipedia API to get artist image URL
def fetch_wikipedia_image(artist_name):
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&piprop=original&titles={artist_name}"
    try:
        response = requests.get(search_url, timeout=5)
        data = response.json()
        pages = data['query']['pages']
        for page_id in pages:
            page = pages[page_id]
            if "original" in page:
                return page["original"]["source"]
    except:
        pass
    # fallback placeholder
    return "https://via.placeholder.com/150?text=No+Image"

# Sample AXII data - replace with your real or API data
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
df = pd.DataFrame(data)

# Fetch trending artists from Artnet
trending_artists = fetch_trending_artnet()

st.sidebar.markdown("### 🔥 Trending on Artnet")
for artist in trending_artists:
    img_url = fetch_wikipedia_image(artist)
    st.sidebar.markdown(f"""
    <div class="sidebar-artist">
        <img src="{img_url}" class="sidebar-artist-image" alt="{artist} image" />
        <div>{artist}</div>
    </div>
    """, unsafe_allow_html=True)

# Artist selection widget including trending artists
all_artists = list(set(df["Artist"].tolist() + trending_artists))
artists_selected = st.multiselect("Select artists to compare:", all_artists, default=df["Artist"].tolist())
filtered_df = df[df["Artist"].isin(artists_selected)]

# Display artist scorecards
st.markdown("### Artist Scores")
cols = st.columns(len(filtered_df)) if len(filtered_df) > 0 else []
for idx, row in filtered_df.iterrows():
    with cols[list(filtered_df.index).index(idx)]:
        st.markdown(f"""
        <div class="metric-card">
            <img src="{row['Image']}" class="artist-image" alt="{row['Artist']} image"/>
            <h3>{row['Artist']}</h3>
            <p><b>CCI:</b> {row['Cultural Capital Index (CCI)']}</p>
            <p><b>EES:</b> {row['Emotional Engagement Score (EES)']}</p>
            <p><b>RSMI:</b> {row['Repeat Sales Market Index (RSMI)']}</p>
        </div>
        """, unsafe_allow_html=True)

# Radar chart
if not filtered_df.empty:
    melted = filtered_df.melt(
        id_vars=["Artist"],
        value_vars=["Cultural Capital Index (CCI)", "Emotional Engagement Score (EES)", "Repeat Sales Market Index (RSMI)"],
        var_name="Index",
        value_name="Score"
    )
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

# Raw data table
st.subheader("Raw AXII Data")
st.dataframe(filtered_df.set_index("Artist"))
