from django.shortcuts import render,get_object_or_404
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=1
    template_name='blog/post/list.html'
def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent=False
    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject=(f"{cd['name']}({cd['email']})",
                     f"{cd['name']}\'s comments:{cd['comments']}")
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(subject=subject,
                      message=message,
                      from_email=None,
                      recipient_list=[cd['to']]
                    )
            sent=True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})
def post_list(request):
    posts=Post.published.all()
    paginator=Paginator(posts,1)
    page_number=request.GET.get('page',1)   
    try:
        posts=paginator.page(page_number)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts=paginator.page(1)
    return render(request,'blog/Post/list.html',{'posts':posts})
def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,
                         slug=post,
                         status=Post.Status.PUBLISHED,
                         publish__year=year,
                         publish__month=month,
                         publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})