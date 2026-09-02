import requests
import os
import datetime
from typing import Dict, List, Any, Tuple

# Base NewsAPI URL
NEWS_API_BASE_URL = "https://newsapi.org/v2"

def fetch_news_articles(
    api_key: str,
    keyword: str = "",
    category: str = "general",
    endpoint: str = "top-headlines",
    page_size: int = 30,
    sort_by: str = "publishedAt"
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Fetches news articles from NewsAPI based on category and keyword filters.

    Args:
        api_key (str): NewsAPI authentication key.
        keyword (str): Search term or keyword.
        category (str): News category (general, technology, business, etc.).
        endpoint (str): 'top-headlines' or 'everything'.
        page_size (int): Number of articles to retrieve (max 100).
        sort_by (str): Sorting criteria for 'everything' endpoint ('publishedAt', 'relevance', 'popularity').

    Returns:
        Tuple[List[Dict[str, Any]], str]: (list of processed article objects, error message if any)
    """
    if not api_key or api_key.strip() == "":
        return get_mock_articles(keyword, category), "NO_API_KEY"

    # Select endpoint target
    if endpoint == "top-headlines":
        url = f"{NEWS_API_BASE_URL}/top-headlines"
        params = {
            "pageSize": min(page_size, 100),
            "apiKey": api_key.strip()
        }
        if category and category != "all":
            params["category"] = category
        if keyword and keyword.strip():
            params["q"] = keyword.strip()
    else:
        # 'everything' endpoint
        url = f"{NEWS_API_BASE_URL}/everything"
        search_q = keyword.strip() if (keyword and keyword.strip()) else category
        if search_q == "all":
            search_q = "latest news"
            
        params = {
            "q": search_q,
            "language": "en",
            "sortBy": sort_by,
            "pageSize": min(page_size, 100),
            "apiKey": api_key.strip()
        }

    headers = {
        "User-Agent": "NewsIntelligenceDashboard/1.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        # Handle HTTP status codes
        if response.status_code == 200:
            data = response.json()
            raw_articles = data.get("articles", [])
            processed_articles = process_raw_articles(raw_articles)
            
            if not processed_articles:
                return [], "EMPTY_RESULTS"
                
            return processed_articles, ""

        elif response.status_code == 401:
            return get_mock_articles(keyword, category), "INVALID_API_KEY"
            
        elif response.status_code == 429:
            return get_mock_articles(keyword, category), "RATE_LIMIT"
            
        elif response.status_code == 400:
            err_msg = response.json().get("message", "Invalid search parameter combination.")
            return [], f"BAD_REQUEST: {err_msg}"
            
        else:
            return [], f"API_ERROR: HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        return [], "TIMEOUT_ERROR"
    except requests.exceptions.ConnectionError:
        return [], "CONNECTION_ERROR"
    except Exception as e:
        return [], f"UNEXPECTED_ERROR: {str(e)}"


def process_raw_articles(raw_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cleans and standardizes raw article dictionaries from NewsAPI.
    """
    cleaned_articles = []
    
    for idx, art in enumerate(raw_articles):
        title = art.get("title") or ""
        # Skip removed or empty articles
        if not title or title.strip() == "[Removed]" or title.strip() == "":
            continue

        source_name = "Unknown Source"
        if art.get("source") and isinstance(art["source"], dict):
            source_name = art["source"].get("name") or "Unknown Source"

        author = art.get("author") or ""
        description = art.get("description") or ""
        content = art.get("content") or ""
        url = art.get("url") or "#"
        if isinstance(url, list) and len(url) > 0:
            url = url[0]
            
        url_to_image = art.get("urlToImage") or ""
        if isinstance(url_to_image, list) and len(url_to_image) > 0:
            url_to_image = url_to_image[0]

        published_at = art.get("publishedAt") or datetime.datetime.now().isoformat()

        # Parse publication date cleanly
        try:
            date_obj = datetime.datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            formatted_date = date_obj.strftime("%b %d, %Y %H:%M")
        except Exception:
            formatted_date = str(published_at)[:16]

        cleaned_articles.append({
            "id": idx + 1,
            "title": title.strip(),
            "source": source_name.strip(),
            "author": author.strip(),
            "description": description.strip(),
            "content": content.strip(),
            "url": url,
            "urlToImage": url_to_image,
            "publishedAt": published_at,
            "formattedDate": formatted_date
        })

    return cleaned_articles


def get_mock_articles(keyword: str = "", category: str = "general") -> List[Dict[str, Any]]:
    """
    Generates high-quality mock news articles matching NewsAPI format.
    """
    now = datetime.datetime.now()
    topic = keyword.capitalize() if keyword else category.capitalize()

    mock_raw = [
        {
            "source": {"id": "the-times-of-india", "name": "The Times of India"},
            "author": "AFP",
            "title": f"Mark Zuckerberg, Elon Musk make plea at G20 for more AI data centers in {topic}",
            "description": f"Mark Zuckerberg and Elon Musk on Tuesday stressed the need for more AI data centers and the electric power needed to support them at a meeting focused on {topic.lower()} innovations.",
            "url": "https://economictimes.indiatimes.com/tech/artificial-intelligence",
            "urlToImage": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&auto=format&fit=crop",
            "publishedAt": (now - datetime.timedelta(hours=1)).isoformat(),
            "content": f"Mark Zuckerberg and Elon Musk stressed the need for more AI data centers..."
        },
        {
            "source": {"id": "financial-times", "name": "Financial Times"},
            "author": "Market Desk",
            "title": f"Global Markets Rally as Economic Policy Updates Boost {topic} Investments",
            "description": f"Stock indices surged today following positive earnings reports and strategic capital allocations across leading {topic.lower()} companies.",
            "url": "https://ft.com",
            "urlToImage": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=600&auto=format&fit=crop",
            "publishedAt": (now - datetime.timedelta(hours=3)).isoformat(),
            "content": "Global stock indices surged today..."
        },
        {
            "source": {"id": "reuters", "name": "Reuters"},
            "author": "Policy Team",
            "title": f"Regulatory Frameworks Tighten Around Data Privacy and {topic} Governance",
            "description": f"International regulatory bodies propose strict compliance standards for consumer data protection and ethical deployment of automated systems in {topic.lower()}.",
            "url": "https://reuters.com",
            "urlToImage": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop",
            "publishedAt": (now - datetime.timedelta(hours=5)).isoformat(),
            "content": "International regulatory bodies propose..."
        },
        {
            "source": {"id": "bloomberg", "name": "Bloomberg"},
            "author": "Logistics Desk",
            "title": f"Supply Chain Disruptions Challenge Growth Projections in {topic} Sector",
            "description": f"Industry experts warn of potential delays and inflation risks impacting hardware production and global shipping networks this quarter.",
            "url": "https://bloomberg.com",
            "urlToImage": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=600&auto=format&fit=crop",
            "publishedAt": (now - datetime.timedelta(hours=8)).isoformat(),
            "content": "Industry experts warn of potential delays..."
        },
        {
            "source": {"id": "techcrunch", "name": "TechCrunch"},
            "author": "Sarah Perez",
            "title": f"Venture Capital Funding Rebounds with Focus on Early-Stage {topic} Startups",
            "description": f"Investors double down on seed-stage funding rounds, signaling renewed confidence in high-margin enterprise software solutions.",
            "url": "https://techcrunch.com",
            "urlToImage": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=600&auto=format&fit=crop",
            "publishedAt": (now - datetime.timedelta(hours=12)).isoformat(),
            "content": "Investors double down on seed-stage funding..."
        }
    ]

    return process_raw_articles(mock_raw)
