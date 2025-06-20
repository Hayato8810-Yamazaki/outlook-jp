from agents.rss_reader_agent import RSSReaderAgent

feed_urls = [
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
]

agent = RSSReaderAgent(feed_urls)
results = agent.run()

for article in results[:3]:
    print(article["title"])
