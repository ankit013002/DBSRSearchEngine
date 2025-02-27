from django.db import models

class CrawledPage(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=500)
    content = models.TextField()

    def __str__(self):
        return self.title
