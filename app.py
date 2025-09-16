from flask import Flask, render_template_string
import feedparser
from datetime import datetime
import pytz  # NEW

app = Flask(__name__)

# RSS feeds from central banks and forex news
RSS_FEEDS = [
    "https://www.ecb.europa.eu/rss/press.html",
    "https://www.bankofengland.co.uk/rss/news",
    "https://www.federalreserve.gov/feeds/press_all.xml",
    "https://www.snb.ch/en/rss",
    "https://www.rba.gov.au/rss/rss-cb-news.xml",
    "https://www.bankofcanada.ca/feed/press-releases/",
    "https://www.dailyfx.com/feeds/market-news",
    "https://www.forexfactory.com/ffcal_week_this.xml"
]

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD"]
NEGATIVE_KEYWORDS = ["cut", "weaker", "dovish", "decline", "down", "fall", "slow"]
POSITIVE_KEYWORDS = ["hike", "stronger", "hawkish", "rise", "up", "gain", "improve"]

def analyze_headlines():
    scores = {cur: 0 for cur in CURRENCIES}
    headlines = []

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:  # limit to latest 20 headlines per source
                title = entry.title.upper()
                headlines.append(title)
                for cur in CURRENCIES:
                    if cur in title:
                        score_change = 1
                        if any(word.upper() in title for word in NEGATIVE_KEYWORDS):
                            score_change = -1
                        elif any(word.upper() in title for word in POSITIVE_KEYWORDS):
                            score_change = 2
                        scores[cur] += score_change
        except Exception:
            continue

    return scores, headlines

@app.route("/")
def index():
    scores, headlines = analyze_headlines()
    strongest = max(scores, key=scores.get)
    weakest = min(scores, key=scores.get)

    # Use Nigeria timezone (Africa/Lagos)
    lagos_tz = pytz.timezone("Africa/Lagos")
    now = datetime.now(lagos_tz).strftime("%Y-%m-%d %H:%M %Z")

    template = '''
    <html>
    <head>
        <title>Currency Strength Dashboard</title>
    </head>
    <body style="font-family: Arial; margin: 40px;">
        <h1>Currency Strength Dashboard</h1>
        <p><b>Last Updated:</b> {{ now }}</p>
        <h2>Strongest Currency: {{ strongest }} (Score: {{ scores[strongest] }})</h2>
        <h2>Weakest Currency: {{ weakest }} (Score: {{ scores[weakest] }})</h2>
        <h3>All Scores:</h3>
        <ul>
            {% for cur, val in scores.items() %}
                <li>{{ cur }}: {{ val }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(template, scores=scores, strongest=strongest, weakest=weakest, now=now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
