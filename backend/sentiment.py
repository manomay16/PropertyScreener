import os
from dotenv import load_dotenv
load_dotenv()

import requests
from nltk.sentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

NEWS_API_URL = "https://newsapi.org/v2/everything"


def get_area_sentiment(city: str, state: str):
    api_key = os.getenv("NEWS_API_KEY")
    query = f"{city} {state}"

    params = {
        "q": query,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
    }

    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        return None

    articles = data.get("articles", [])
    if not articles:
        return None

    scores = []
    for article in articles:
        text = f"{article.get('title', '')}. {article.get('description', '')}"
        sentiment = analyzer.polarity_scores(text)
        scores.append(sentiment["compound"])

    average_sentiment = sum(scores) / len(scores)

    return {
        "average_sentiment": average_sentiment,
        "article_count": len(scores),
    }
