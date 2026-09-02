import streamlit as st
import os
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import modular services and UI components
from services.news_service import fetch_news_articles
from services.text_processor import (
    process_articles_dataframe,
    extract_keywords,
    extract_topics,
    calculate_dashboard_metrics
)
from services.gemini_service import generate_gemini_insights
from ui.components import (
    inject_custom_css,
    render_header,
    render_kpi_metrics,
    plot_sentiment_donut,
    plot_top_keywords,
    plot_sources_bar,
    plot_timeline,
    render_news_feed
)

# Set page configuration
st.set_page_config(
    page_title="Real-Time AI News Intelligence Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom modern CSS
inject_custom_css()

# Retrieve API keys securely from environment / .env file (not displayed on Streamlit UI)
effective_news_key = os.getenv("NEWS_API_KEY", "").strip()
effective_gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
is_live = bool(effective_news_key)

# Initialize session state variables
if "articles_df" not in st.session_state:
    st.session_state["articles_df"] = None
if "insights_cache" not in st.session_state:
    st.session_state["insights_cache"] = None
if "last_fetch_time" not in st.session_state:
    st.session_state["last_fetch_time"] = ""

# --- SIDEBAR NAVIGATION & FILTERS ---
st.sidebar.markdown("## 📍 Navigation")
navigation = st.sidebar.radio(
    "Select View",
    options=["🏠 Home (News Stream)", "📊 Sentiment & AI Analytics"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("## 🔍 Search & Filters")

# Keyword Search
search_keyword = st.sidebar.text_input(
    "Keyword Search",
    value="",
    placeholder="e.g. Artificial Intelligence, Zuckerberg, Markets..."
)

# Category Selection
category_options = ["general", "technology", "business", "sports", "entertainment", "health", "science"]
selected_category = st.sidebar.selectbox("Category", options=category_options, index=1)

# Article Count Limit
article_count = st.sidebar.slider("Number of Articles", min_value=10, max_value=100, value=30, step=10)

# Refresh Button
refresh_clicked = st.sidebar.button("🔄 Fetch & Refresh News", use_container_width=True, type="primary")

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="font-size: 0.78rem; color: #64748B; text-align: center; margin-top: 1.5rem;">
    Real-Time AI News Intelligence Dashboard<br>
    Powered by <b>Streamlit • NewsAPI • Gemini AI</b>
</div>
""", unsafe_allow_html=True)


# --- MAIN CONTENT AREA ---

# Render Header Banner with status pill
render_header(api_connected=is_live, last_updated=st.session_state["last_fetch_time"])

# Determine if news fetch should run
should_fetch = refresh_clicked or st.session_state["articles_df"] is None

if should_fetch:
    with st.spinner("⚡ Fetching real-time news articles & calculating NLP metrics..."):
        raw_articles, err_code = fetch_news_articles(
            api_key=effective_news_key,
            keyword=search_keyword,
            category=selected_category,
            page_size=article_count
        )

        # Handle API Error Warnings
        if err_code == "NO_API_KEY":
            st.warning("⚠️ **NewsAPI Key missing in `.env` file.** Displaying sample news data for demonstration. Set `NEWS_API_KEY` in your `.env` file to fetch live news.")
        elif err_code == "INVALID_API_KEY":
            st.error("❌ **Invalid NewsAPI Key in `.env`.** Showing fallback sample data. Please verify your API key in `.env` file.")
        elif err_code == "RATE_LIMIT":
            st.warning("⚠️ **NewsAPI Rate Limit hit.** Displaying cached/sample dataset.")
        elif err_code == "EMPTY_RESULTS":
            st.info("ℹ️ No news articles matched your search query. Try broadening your keyword or category.")
        elif err_code and not err_code.startswith("BAD_REQUEST"):
            st.error(f"⚠️ News fetch status: {err_code}")

        # Process articles into DataFrame & analytics
        df = process_articles_dataframe(raw_articles)
        st.session_state["articles_df"] = df
        st.session_state["insights_cache"] = None # Reset AI insights cache on fresh fetch
        st.session_state["last_fetch_time"] = datetime.datetime.now().strftime("%H:%M:%S")
else:
    df = st.session_state["articles_df"]

if df is not None and not df.empty:
    metrics = calculate_dashboard_metrics(df)
    keywords = extract_keywords(df.to_dict("records"), top_n=15)
    topics = extract_topics(df.to_dict("records"), top_n=6)

    # 1. Render Top KPI Metric Cards (Always Visible)
    render_kpi_metrics(metrics)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- VIEW 1: HOME (NEWS CARDS & FEED) ---
    if navigation == "🏠 Home (News Stream)":
        st.markdown('<div class="section-title">📰 Live News Cards Feed</div>', unsafe_allow_html=True)

        # Quick filter box for loaded articles
        filter_query = st.text_input("Filter loaded articles:", placeholder="Search title, description, or publisher...")
        if filter_query.strip():
            display_df = df[
                df["title"].str.contains(filter_query, case=False, na=False) |
                df["description"].str.contains(filter_query, case=False, na=False) |
                df["source"].str.contains(filter_query, case=False, na=False)
            ]
        else:
            display_df = df

        render_news_feed(display_df)

    # --- VIEW 2: SENTIMENT & AI ANALYTICS ---
    elif navigation == "📊 Sentiment & AI Analytics":
        # Gemini AI Insights Section
        st.markdown('<div class="section-title">🤖 Google Gemini Executive Synthesis</div>', unsafe_allow_html=True)
        
        if st.session_state["insights_cache"] is None:
            with st.spinner("🤖 Synthesizing executive intelligence via Google Gemini AI..."):
                ai_insights = generate_gemini_insights(
                    df=df,
                    keywords=keywords,
                    metrics=metrics,
                    api_key=effective_gemini_key,
                    category=selected_category,
                    keyword_filter=search_keyword
                )
                st.session_state["insights_cache"] = ai_insights
        else:
            ai_insights = st.session_state["insights_cache"]

        st.markdown(f"""
        <div class="ai-insights-box">
            <span class="ai-badge">🤖 ✨ Gemini 2.5 Intelligence Engine</span>
            <div>{ai_insights}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Interactive Visual News Analytics</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            plot_sentiment_donut(df)
        with c2:
            plot_top_keywords(keywords)

        st.markdown("<br>", unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            plot_sources_bar(df)
        with c4:
            plot_timeline(df)

        if topics:
            st.markdown("#### 🔥 Emerging Topic Clusters")
            topic_html = " ".join([
                f'<span class="badge badge-neutral" style="font-size:0.85rem; padding: 0.4rem 0.85rem; margin: 0.2rem;">🏷️ {title} ({cnt})</span>'
                for title, cnt in topics
            ])
            st.markdown(topic_html, unsafe_allow_html=True)

else:
    st.info("👈 Use the sidebar filters and click **Fetch & Refresh News** to begin.")
