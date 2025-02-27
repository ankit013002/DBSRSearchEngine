import scrapy
from bs4 import BeautifulSoup
from webcrawler.items import CrawledPageItem

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["wikipedia.org", "en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Web_crawler"]  # Start from a specific article

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        item = CrawledPageItem()
        item["url"] = response.url
        item["title"] = soup.title.string.strip() if soup.title else "No Title"
        item["content"] = " ".join(p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)).strip()

        # Extract title and body text safely
        title = soup.title.string.strip() if soup.title else "No Title"
        body_text = " ".join(p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True))

        yield {
            "url": response.url,
            "title": title,
            "content": body_text.strip(),
        }

        # Follow only Wikipedia article links (avoid non-article pages)
        for link in soup.find_all("a", href=True):
            relative_url = link["href"]

            # Ensure it's an article link and filter out special pages (e.g., Help, File, Talk, etc.)
            if relative_url.startswith("/wiki/") and ":" not in relative_url:
                absolute_url = response.urljoin(relative_url)

                # Let Scrapy handle duplicate requests instead of using a class variable
                yield scrapy.Request(absolute_url, callback=self.parse)
