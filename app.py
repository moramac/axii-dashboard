# ... [rest of your imports and previous code]

st.markdown('<div class="big-title">AXII Artist Intelligence Dashboard</div>', unsafe_allow_html=True)

# About / Introduction section
st.markdown("""
### About AXII Dashboard

The **AXII (Artist eXperience & Impact Index)** Dashboard is designed to bring transparency and data-driven insights into the contemporary art market, focusing on measuring artists’ cultural capital, emotional engagement, and market activity.

**Purpose:**  
This platform aggregates multiple data sources—news media mentions, social media engagement, and auction sales data—to create a comprehensive index reflecting an artist’s influence and market momentum.

**Why AXII?**  
Traditional art market analytics often overlook the consumer psychology and cultural context that drive art value. AXII aims to bridge that gap by combining quantitative data with qualitative signals, enabling collectors, galleries, and art enthusiasts to better understand emerging and established artists.

**How It Works:**  
- **Cultural Capital Index (CCI):** Measured by recent news media coverage through APIs like NewsAPI.  
- **Emotional Engagement Score (EES):** Estimated using social media engagement metrics, simulated here for demonstration.  
- **Repeat Sales Market Index (RSMI):** Derived from auction house sales volume and frequency scraped from Phillips and similar platforms.

**Data Sources:**  
- NewsAPI.org for media mentions  
- Web scraping of auction results from Phillips (expandable to Christie’s, Sotheby’s)  
- Wikipedia and other open sources for artist imagery

**Development:**  
Built with Streamlit and Python, this MVP is an evolving prototype aimed at illustrating the potential of transparent, real-time art market analytics.

---

Feel free to contribute, suggest improvements, or request new features!  
""")

# ... [rest of your existing app code follows]
