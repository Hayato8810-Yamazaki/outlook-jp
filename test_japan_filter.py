from agents.japan_filter_agent import JapanFilterAgent
from schemas.rss_schema import Article

articles = [
    Article(title="Kishida meets Biden in Washington", description="Discussing economic ties"),
    Article(title="Elections in Germany", description="Politicians debate"),
]

filtered = JapanFilterAgent().run(articles)

for a in filtered:
    print(a.title)
