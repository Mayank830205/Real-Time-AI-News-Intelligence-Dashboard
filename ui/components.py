import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime
from typing import List, Dict, Any, Tuple

def inject_custom_css():
    """
    Injects modern, professional CSS styles into the Streamlit app.
    Supports both light and dark Streamlit themes with custom visual hierarchy.
    """
    st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main container padding */
    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
        max-width: 1280px;
    }
    
    /* Header banner styling */
    .header-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #312E81 100%);
        color: #F8FAFC;
        padding: 1.6rem 2.2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        margin-bottom: 1.8rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    
    .header-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .header-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
        font-weight: 400;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 0.35rem 0.85rem;
        border-radius: 30px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    .status-pill-demo {
        background: rgba(245, 158, 11, 0.12);
        color: #FBBF24;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #34D399;
        border-radius: 50%;
        box-shadow: 0 0 8px #34D399;
    }

    .status-dot-demo {
        background-color: #FBBF24;
        box-shadow: 0 0 8px #FBBF24;
    }

    /* KPI Metric Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        position: relative;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
        border-color: #CBD5E1;
    }

    .kpi-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .kpi-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.5px;
    }

    .kpi-icon {
        font-size: 1.1rem;
        opacity: 0.8;
    }

    .kpi-value-main {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }

    .kpi-subtext {
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 0.35rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    /* Sentiment badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.22rem 0.65rem;
        font-size: 0.72rem;
        font-weight: 600;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    
    .badge-positive {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }
    
    .badge-negative {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
    }
    
    .badge-neutral {
        background-color: #F8FAFC;
        color: #475569;
        border: 1px solid #E2E8F0;
    }

    /* Gemini AI Insights Container */
    .ai-insights-box {
        background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 50%, #EEF2FF 100%);
        border: 1px solid #D8B4FE;
        border-left: 6px solid #9333EA;
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(147, 51, 234, 0.08);
    }

    .ai-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #9333EA;
        color: #FFFFFF;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }

    /* News Cards */
    .news-card-wrapper {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease-in-out;
    }

    .news-card-wrapper:hover {
        border-color: #93C5FD;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.08);
    }

    .news-meta-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .news-publisher {
        font-size: 0.8rem;
        font-weight: 700;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .news-author {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 500;
    }

    .news-date {
        font-size: 0.78rem;
        color: #94A3B8;
    }

    .news-card-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0.4rem 0 0.6rem 0;
        line-height: 1.4;
    }

    .news-card-desc {
        font-size: 0.91rem;
        color: #475569;
        line-height: 1.55;
        margin-bottom: 0.9rem;
    }

    .read-more-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        color: #2563EB;
        font-size: 0.86rem;
        font-weight: 600;
        text-decoration: none;
        transition: color 0.15s ease;
    }

    .read-more-btn:hover {
        color: #1D4ED8;
        text-decoration: underline;
    }

    /* Section headers */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(api_connected: bool = True, last_updated: str = ""):
    """
    Renders a modern executive header banner with live API status pill.
    """
    status_class = "status-pill" if api_connected else "status-pill status-pill-demo"
    dot_class = "status-dot" if api_connected else "status-dot status-dot-demo"
    status_text = "LIVE API CONNECTED" if api_connected else "DEMO MODE (SAMPLE DATA)"
    
    updated_str = f" • Updated {last_updated}" if last_updated else ""

    st.markdown(f"""
    <div class="header-container">
        <div class="header-title-row">
            <div>
                <h1 class="header-title">📰 Real-Time AI News Intelligence</h1>
                <p class="header-subtitle">Live news curation, NLP sentiment analytics, and AI executive synthesis with Google Gemini.</p>
            </div>
            <div class="{status_class}">
                <span class="{dot_class}"></span>
                {status_text}{updated_str}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_metrics(metrics: Dict[str, Any], is_sentiment_view: bool = False):
    """
    Renders 5 responsive KPI cards across top of dashboard.
    """
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label">Total Articles</span>
                <span class="kpi-icon">📦</span>
            </div>
            <div class="kpi-value-main">{metrics['total_articles']}</div>
            <div class="kpi-subtext">Articles Processed</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label">Positive News</span>
                <span class="kpi-icon">🟢</span>
            </div>
            <div class="kpi-value-main" style="color: #059669;">{metrics['positive_pct']}%</div>
            <div class="kpi-subtext">▲ {metrics['positive_count']} Articles</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label">Neutral News</span>
                <span class="kpi-icon">⚪</span>
            </div>
            <div class="kpi-value-main" style="color: #64748B;">{metrics['neutral_pct']}%</div>
            <div class="kpi-subtext">● {metrics['neutral_count']} Articles</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label">Negative News</span>
                <span class="kpi-icon">🔴</span>
            </div>
            <div class="kpi-value-main" style="color: #DC2626;">{metrics['negative_pct']}%</div>
            <div class="kpi-subtext">▼ {metrics['negative_count']} Articles</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        top_src = metrics['top_source']
        if len(top_src) > 16:
            top_src = top_src[:14] + ".."
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header-row">
                <span class="kpi-label">Top Publisher</span>
                <span class="kpi-icon">🔥</span>
            </div>
            <div class="kpi-value-main" style="font-size: 1.3rem; padding-top: 0.2rem;">{top_src}</div>
            <div class="kpi-subtext">Dominant Source</div>
        </div>
        """, unsafe_allow_html=True)


def plot_sentiment_donut(df: pd.DataFrame):
    """
    Renders an interactive Plotly Donut Chart for sentiment distribution.
    """
    if df.empty or "sentiment" not in df.columns:
        st.info("No sentiment data available.")
        return

    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["Sentiment", "Count"]

    color_map = {
        "Positive": "#10B981",
        "Neutral": "#64748B",
        "Negative": "#EF4444"
    }

    fig = px.pie(
        counts,
        names="Sentiment",
        values="Count",
        hole=0.6,
        color="Sentiment",
        color_discrete_map=color_map,
        title="<b>Sentiment Share</b>"
    )

    fig.update_traces(
        textposition="inside", 
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=40, b=40),
        height=330
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_top_keywords(keywords_tuples: List[Tuple[str, int]]):
    """
    Renders an interactive horizontal bar chart for top keywords.
    """
    if not keywords_tuples:
        st.info("No keyword data available.")
        return

    kw_df = pd.DataFrame(keywords_tuples[:10], columns=["Keyword", "Frequency"]).sort_values("Frequency", ascending=True)

    fig = px.bar(
        kw_df,
        x="Frequency",
        y="Keyword",
        orientation="h",
        title="<b>Top Extracted Keywords</b>",
        color="Frequency",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        xaxis_title="Frequency",
        yaxis_title=None,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=330
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_sources_bar(df: pd.DataFrame):
    """
    Renders a bar chart of top news publishers.
    """
    if df.empty or "source" not in df.columns:
        st.info("No source data available.")
        return

    src_counts = df["source"].value_counts().head(7).reset_index()
    src_counts.columns = ["Publisher", "Article Count"]

    fig = px.bar(
        src_counts,
        x="Publisher",
        y="Article Count",
        title="<b>Articles by News Publisher</b>",
        color="Article Count",
        color_continuous_scale="Purples"
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Articles",
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=330
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_timeline(df: pd.DataFrame):
    """
    Renders publication timeline distribution.
    """
    if df.empty or "publishedAt" not in df.columns:
        st.info("No timeline data available.")
        return

    temp_df = df.copy()
    try:
        temp_df["dt"] = pd.to_datetime(temp_df["publishedAt"], errors='coerce')
        temp_df["Hour"] = temp_df["dt"].dt.strftime("%b %d, %H:00")
        timeline = temp_df["Hour"].value_counts().reset_index()
        timeline.columns = ["Time Slot", "Articles"]
        timeline = timeline.sort_values("Time Slot")

        fig = px.line(
            timeline,
            x="Time Slot",
            y="Articles",
            markers=True,
            title="<b>Publication Volume Over Time</b>",
            line_shape="spline"
        )

        fig.update_traces(line_color="#6366F1", line_width=3)
        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Count",
            margin=dict(l=20, r=20, t=40, b=20),
            height=330
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("Publication timestamp formatting unavailable for chart.")


def render_news_feed(df: pd.DataFrame):
    """
    Renders news articles in clean, modern card layouts containing
    Title, Description, Image, Source/Author, Published Date, and Link.
    """
    if df.empty:
        st.info("No news articles available matching your query.")
        return

    for idx, row in df.iterrows():
        sentiment = row.get("sentiment", "Neutral")
        if sentiment == "Positive":
            badge_html = '<span class="badge badge-positive">▲ Positive</span>'
        elif sentiment == "Negative":
            badge_html = '<span class="badge badge-negative">▼ Negative</span>'
        else:
            badge_html = '<span class="badge badge-neutral">● Neutral</span>'

        img_url = row.get("urlToImage")
        has_image = bool(img_url and isinstance(img_url, str) and img_url.startswith("http"))
        author_text = f" • By {row.get('author')}" if row.get("author") else ""
        source_label = f"{row.get('source', 'News')}{author_text}"

        card_content = f"""
        <div class="news-card-wrapper">
            <div class="news-meta-row">
                <div>
                    <span class="news-publisher">{source_label}</span>
                    &nbsp;•&nbsp; {badge_html}
                </div>
                <span class="news-date">📅 {row.get('formattedDate', '')}</span>
            </div>
            <div class="news-card-title">{row.get('title', 'Untitled Article')}</div>
            <div class="news-card-desc">{row.get('description', 'No description available for this article.')}</div>
            <div>
                <a href="{row.get('url', '#')}" target="_blank" class="read-more-btn">
                    Read Full Article 🔗
                </a>
            </div>
        </div>
        """

        container = st.container()
        with container:
            if has_image:
                col_img, col_text = st.columns([1, 3])
                with col_img:
                    try:
                        st.image(img_url, use_container_width=True)
                    except Exception:
                        st.markdown("📰")
                with col_text:
                    st.markdown(card_content, unsafe_allow_html=True)
            else:
                st.markdown(card_content, unsafe_allow_html=True)
