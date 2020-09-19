from django.urls import reverse_lazy
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


class LatestPostsFeed(Feed):
    title = "My Blog"
    link = reverse_lazy("blog:post_list")
    description = "New posts of the blog"
    
    @staticmethod
    def items():
        return Post.published.all()[:5]
    
    def item_title(self, item: Post):
        return item.title
    
    def item_description(self, item: Post):
        return truncatewords(item.body, 30)
