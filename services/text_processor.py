import re
import pandas as pd
from collections import Counter
from typing import List, Dict, Any, Tuple

# Try importing vaderSentiment; fallback to basic sentiment engine if not installed
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader_analyzer = SentimentIntensityAnalyzer()
    HAS_VADER = True
except ImportError:
    HAS_VADER = False

# Standard set of English stopwords for clean keyword extraction
ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can",
    "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
    "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
    "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
    "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
    "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
    "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves", "said", "says", "new", "news", "report", "according", "market", "year", "first", "one",
    "two", "also", "per", "via", "us", "uk", "world", "today", "latest", "update", "day", "week"
}

def analyze_sentiment(text: str) -> Tuple[str, float]:
    """
    Analyzes sentiment of a given text snippet using VADER or keyword heuristics.

    Returns:
        Tuple[str, float]: (Sentiment label: 'Positive'/'Negative'/'Neutral', Compound score)
    """
    if not text or not text.strip():
        return "Neutral", 0.0

    if HAS_VADER:
        scores = vader_analyzer.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            return "Positive", compound
        elif compound <= -0.05:
            return "Negative", compound
        else:
            return "Neutral", compound
    else:
        # Simple lexicon fallback if VADER unavailable
        pos_words = {"boost", "gain", "growth", "breakthrough", "success", "record", "rally", "positive", "high", "soar", "profit", "win"}
        neg_words = {"drop", "fall", "decline", "crisis", "threat", "warning", "attack", "risk", "loss", "slash", "cut", "fail", "delay"}
        
        tokens = set(re.findall(r'\w+', text.lower()))
        pos_count = len(tokens.intersection(pos_words))
        neg_count = len(tokens.intersection(neg_words))
        
        score = (pos_count - neg_count) / max(len(tokens), 1)
        if score > 0.02:
            return "Positive", score
        elif score < -0.02:
            return "Negative", score
        else:
            return "Neutral", 0.0


def extract_keywords(articles: List[Dict[str, Any]], top_n: int = 15) -> List[Tuple[str, int]]:
    """
    Extracts most frequent meaningful words from headlines and descriptions.
    """
    text_corpus = []
    for art in articles:
        title = art.get("title") or ""
        desc = art.get("description") or ""
        text_corpus.append(f"{title} {desc}")

    combined_text = " ".join(text_corpus).lower()
    # Extract alphanumeric words length >= 3
    words = re.findall(r'\b[a-z]{3,}\b', combined_text)
    
    # Filter stopwords
    filtered_words = [w for w in words if w not in ENGLISH_STOPWORDS]
    
    counter = Counter(filtered_words)
    return counter.most_common(top_n)


def extract_topics(articles: List[Dict[str, Any]], top_n: int = 6) -> List[Tuple[str, int]]:
    """
    Extracts key bi-grams / multi-word topic phrases from news headlines.
    """
    phrases = []
    for art in articles:
        title = art.get("title") or ""
        # Clean headline
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
        meaningful = [w for w in words if w not in ENGLISH_STOPWORDS]
        
        # Form bi-grams
        for i in range(len(meaningful) - 1):
            phrase = f"{meaningful[i]} {meaningful[i+1]}"
            phrases.append(phrase.title())

    counter = Counter(phrases)
    return counter.most_common(top_n)


def process_articles_dataframe(articles: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Converts article list to a pandas DataFrame with sentiment scores and formatted dates.
    """
    if not articles:
        return pd.DataFrame(columns=[
            "id", "title", "source", "description", "content", "url", 
            "urlToImage", "publishedAt", "formattedDate", "sentiment", "sentiment_score"
        ])

    df = pd.DataFrame(articles)

    # Perform sentiment analysis on combined title + description
    sentiments = []
    scores = []
    
    for idx, row in df.iterrows():
        text = f"{row.get('title', '')}. {row.get('description', '')}"
        label, score = analyze_sentiment(text)
        sentiments.append(label)
        scores.append(score)

    df["sentiment"] = sentiments
    df["sentiment_score"] = scores

    return df


def calculate_dashboard_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculates summary aggregate KPIs for the dashboard.
    """
    total = len(df)
    if total == 0:
        return {
            "total_articles": 0,
            "positive_count": 0,
            "neutral_count": 0,
            "negative_count": 0,
            "positive_pct": 0.0,
            "neutral_pct": 0.0,
            "negative_pct": 0.0,
            "top_source": "N/A"
        }

    sentiment_counts = df["sentiment"].value_counts().to_dict()
    pos = sentiment_counts.get("Positive", 0)
    neu = sentiment_counts.get("Neutral", 0)
    neg = sentiment_counts.get("Negative", 0)

    top_source = df["source"].mode()[0] if not df["source"].empty else "N/A"

    return {
        "total_articles": total,
        "positive_count": pos,
        "neutral_count": neu,
        "negative_count": neg,
        "positive_pct": round((pos / total) * 100, 1),
        "neutral_pct": round((neu / total) * 100, 1),
        "negative_pct": round((neg / total) * 100, 1),
        "top_source": top_source
    }
