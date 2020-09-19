from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Post.published.all()
    
    @staticmethod
    def lastmode(obj: Post):
        return obj.updated
