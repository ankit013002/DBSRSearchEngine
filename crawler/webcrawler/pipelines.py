import sys
import os
import django
import logging
import unicodedata

# Set up Django's environment inside Scrapy
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "searchengine.settings")
django.setup()

print("PROJECT_ROOT is", PROJECT_ROOT)

from crawler.models import CrawledPage

class SaveToDatabasePipeline:
    def process_item(self, item, spider):
        try:
            normalized_title = unicodedata.normalize("NFKD", item.get("title", ""))
            normalized_content = unicodedata.normalize("NFKD", item.get("content", ""))

            if not CrawledPage.objects.filter(url=item["url"]).exists():
                CrawledPage.objects.create(
                    url=item["url"],
                    title=normalized_title,
                    content=normalized_content,
                )
                logging.info(f"Saved {item['url']} to database.")
            else:
                logging.info(f"Skipped {item['url']} (already exists).")
        except Exception as e:
            logging.error(f"Error saving {item['url']} to database: {e}", exc_info=True)
        return item
