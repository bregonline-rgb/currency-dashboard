from flask import Flask, render_template_string
import feedparser

app = Flask(__name__)

CENTRAL_BANK_FEEDS = {
    "USD": "https://www.federalreserve.gov/feeds/press_all.xml",
    "EUR": "https://www.ecb.europa.eu/press/rss/press.xml",
    "GBP": "https://www.bankofengland.co.uk/rss/news",
    "JPY": "https://www.boj.or.jp/en/rss/whatsnew.xml",
}

KEYWORDS_HAWKISH = ["rate hike", "inflation", "tightening", "raise rates", "strong economy"]
KEYWORDS_DOVISH = ["rate cut", "stimulus", "easing", "weak economy", "slowdown"]

def analyze_feed(feed_url):
    d = feedparser.parse(feed_url)
    score = 0
    headlines = []
    for entry in d.entries[:5]:
        title = entry.title.lower()
        headlines.append(entry.title)
        if any(word in title for word in KEYWORDS_HAWKISH):
            score += 1
        if any(word in title for word in KEYWORDS_DOVISH):
            score -= 1
    return score, headlines

@app.route('/')
def dashboard():
    scores = {}
    headlines_data = {}
    for currency, url in CENTRAL_BANK_FEEDS.items():
        score, headlines = analyze_feed(url)
        scores[currency] = score
        headlines_data[currency] = headlines

    strongest = max(scores, key=scores.get)
    weakest = min(scores, key=scores.get)

    html = """
    <html>
    <head><title>Currency Strength Dashboard</title></head>
    <body style="font-family: Arial; margin: 40px;">
      <h1>Currency Strength Monitor</h1>
      <h2>Strongest: {{ strongest }}</h2>
      <h2>Weakest: {{ weakest }}</h2>
      <h3>Scores:</h3>
      <ul>
      {% for c, s in scores.items() %}
        <li>{{ c }}: {{ s }}</li>
      {% endfor %}
      </ul>
      <h3>Latest Headlines:</h3>
      {% for c, heads in headlines.items() %}
        <h4>{{ c }}</h4>
        <ul>
        {% for h in heads %}
          <li>{{ h }}</li>
        {% endfor %}
        </ul>
      {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, strongest=strongest, weakest=weakest, scores=scores, headlines=headlines_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
