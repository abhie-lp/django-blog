from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

#def post_list(request):
#    object_list = Post.published.all()
#    paginator = Paginator(object_list, 3)
#    page = request.GET.get("page")
#    try:
#        posts = paginator.page(page)
#    except PageNotAnInteger:
#        # If not an integer deliver the first page
#        posts = paginator.page(1)
#    except EmptyPage:
#        # If page is out of range deliver last page of results
#        posts = paginator.page(paginator.num_pages)
#
#    return render(request, "blog/list.html", {"page": page, "posts": posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/list.html"


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status="published",
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)

    return render(request, "blog/detail.html", {"post": post})


from .forms import EmailPostForm
from django.core.mail import send_mail

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you reading {post.title}."
            message = f'Read "{post.title}" at {post_url}\n\n{cd["name"]}\'s comments {cd["comments"]}.'
            send_mail(subject, message, "admin@myblog.com", [cd["to"]])
            sent = True
    
    else:
        form = EmailPostForm()
    
    return render(request, "blog/share.html", {"post": post, "form": form, "sent": sent})