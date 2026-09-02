import os
import pandas as pd
from typing import Dict, Any, List

def generate_gemini_insights(
    df: pd.DataFrame,
    keywords: List[tuple],
    metrics: Dict[str, Any],
    api_key: str = "",
    category: str = "general",
    keyword_filter: str = ""
) -> str:
    """
    Sends processed news data to Google Gemini API to generate executive AI news intelligence.

    Args:
        df (pd.DataFrame): DataFrame of processed news articles.
        keywords (List[tuple]): List of top extracted keyword tuples (word, count).
        metrics (Dict[str, Any]): Summary KPI dict.
        api_key (str): Google Gemini API Key.
        category (str): Selected category.
        keyword_filter (str): User keyword filter.

    Returns:
        str: Formatted markdown containing Gemini AI insights.
    """
    if df.empty:
        return "⚠️ *No news data available to analyze. Please adjust your search filters.*"

    # If no API key provided, return smart mock insights with setup instructions
    if not api_key or api_key.strip() == "":
        return generate_heuristic_fallback_insights(df, keywords, metrics, category, keyword_filter)

    # Construct concise structured prompt
    headlines_summary = "\n".join([
        f"- [{row['source']}] {row['title']} (Sentiment: {row['sentiment']})"
        for _, row in df.head(12).iterrows()
    ])

    top_kw_str = ", ".join([f"{word} ({count})" for word, count in keywords[:10]])
    focus_topic = keyword_filter.strip() if keyword_filter.strip() else category

    prompt = f"""
You are an expert AI News Intelligence Analyst. Analyze the following real-time news dataset for the focus topic/category: "{focus_topic}".

DATA SUMMARY:
- Total Articles Analyzed: {metrics['total_articles']}
- Sentiment Breakdown: {metrics['positive_pct']}% Positive, {metrics['neutral_pct']}% Neutral, {metrics['negative_pct']}% Negative
- Dominant News Publisher: {metrics['top_source']}
- Top Extracted Keywords: {top_kw_str}

SAMPLE HEADLINES & SENTIMENTS:
{headlines_summary}

TASK:
Provide an executive, concise, and structured News Intelligence Report in Markdown with 4 distinct sections:

1. 📌 **Executive News Summary**
   - Provide a 2-3 sentence high-level overview of what is happening in the news right now regarding {focus_topic}.

2. 💡 **Key Insights & Market Signals**
   - List 3 key strategic takeaways, trends, or underlying factors driving current coverage.

3. 🔥 **Trending Topics & Emerging Themes**
   - Identify 2-3 prominent sub-topics or emerging themes based on the headlines.

4. ⚖️ **Overall Sentiment & Outlook**
   - Evaluate the overall tone of the media coverage and what it implies for near-term developments.

Keep your formatting crisp, professional, bulleted, and ready for executive presentation.
"""

    # Call Gemini API using available SDK
    try:
        # First try google.genai (new standard SDK)
        try:
            from google import genai
            client = genai.Client(api_key=api_key.strip())
            
            # Try available model names
            for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    if response and response.text:
                        return response.text
                except Exception:
                    continue
        except ImportError:
            pass

        # Fallback to google.generativeai (legacy SDK)
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key.strip())
            
            for model_name in ["gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro"]:
                try:
                    model = genai_legacy.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    if response and response.text:
                        return response.text
                except Exception:
                    continue
        except ImportError:
            pass

        # If API call attempts were unsuccessful due to key permissions or model availability
        return generate_heuristic_fallback_insights(
            df, keywords, metrics, category, keyword_filter, 
            notice="*(Notice: Gemini API key check failed or rate limit hit. Displaying automated smart summary fallback below.)*\n\n"
        )

    except Exception as e:
        return generate_heuristic_fallback_insights(
            df, keywords, metrics, category, keyword_filter, 
            notice=f"*(Notice: Gemini API call error: {str(e)}. Displaying automated fallback below.)*\n\n"
        )


def generate_heuristic_fallback_insights(
    df: pd.DataFrame,
    keywords: List[tuple],
    metrics: Dict[str, Any],
    category: str,
    keyword_filter: str,
    notice: str = ""
) -> str:
    """
    Generates intelligent structured rule-based news insights when Gemini API key is missing or fails.
    """
    topic = keyword_filter.strip().capitalize() if keyword_filter.strip() else category.capitalize()
    top_kw_str = ", ".join([w[0] for w in keywords[:5]]) if keywords else "technology, markets, global"
    
    top_headlines = df["title"].head(3).tolist()
    headline_list_str = "\n".join([f"  - *{h}*" for h in top_headlines])

    sent_label = "predominantly positive" if metrics["positive_pct"] > 40 else (
        "predominantly cautious/negative" if metrics["negative_pct"] > 40 else "balanced and neutral"
    )

    fallback_text = f"""{notice}📌 **Executive News Summary**
Current media coverage surrounding **{topic}** indicates active reporting with a total of **{metrics['total_articles']} articles** processed. Key publishers such as **{metrics['top_source']}** are actively tracking major developments and strategic announcements.

Headline Spotlights:
{headline_list_str}

💡 **Key Insights & Market Signals**
- **Media Attention**: Coverage is heavily concentrated around core drivers including **{top_kw_str}**.
- **Sentiment Tone**: The overall tone across reported stories is **{sent_label}**, with positive stories accounting for {metrics['positive_pct']}% of total volume.
- **Publisher Density**: **{metrics['top_source']}** represents the leading distribution node for news in this iteration.

🔥 **Trending Topics & Emerging Themes**
- **Core Vector**: Digital transformation, economic adjustments, and regulatory policy shifts.
- **High-Frequency Keywords**: `{top_kw_str}`.

⚖️ **Overall Sentiment & Outlook**
With **{metrics['positive_pct']}% Positive**, **{metrics['neutral_pct']}% Neutral**, and **{metrics['negative_pct']}% Negative** articles, the market outlook for **{topic}** suggests stability with ongoing observation of macro trends.

---
> 💡 *To enable full AI-generated synthesis from Google Gemini, add your `GEMINI_API_KEY` to the `.env` file or enter it in the Streamlit sidebar!*
"""
    return fallback_text
