from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import BlogPost
from .forms import CreateBlogPost

# Create your views here.
def home_page(request):
    blogs = BlogPost.objects.order_by('-timestamp')

    if 'q' in request.GET:
        query = request.GET.get('q', None)
        lookups = Q(title__icontains=query) | Q(body__icontains=query) | Q(tag__title__icontains=query)
        blogs = blogs.filter(lookups).distinct()

    paginator = Paginator(blogs, 5)
    page = request.GET.get('page', None)
    paged_blogs = paginator.get_page(page)

    context = {
        "blogs" : paged_blogs
    }
    return render(request, 'home.html', context)


def blog_details(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    if blog is not None:
        blog.views += 1
        blog.save()
    context = {
        "blog" : blog
    }
    return render(request, 'details.html', context)


class CreateBlog(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    # model = BlogPost
    # fields = ['title', 'body']
    form_class = CreateBlogPost
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        post_form = form.save(commit=False)
        if user.is_authenticated:
            post_form.user = user
        else:
            post_form.user = get_object_or_404(get_user_model(), id=1)
        post_form.save()
        return super().form_valid(form)


class EditBlogView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'edit.html'
    model = BlogPost
    form_class = CreateBlogPost
    # fields = '__all__'
    success_message = "Post updated successfully."

    def get_object(self, *args, **kwargs):
        blog = super(EditBlogView, self).get_object(*args, **kwargs)
        user = self.request.user
        if user != blog.user:
            messages.error(self.request, "Permission Denied: You cannot edit anyone else's post.")
            raise PermissionDenied
        return blog


@login_required(login_url='/accounts/login/')
def delete_post(request, slug):
    user = request.user
    blog = get_object_or_404(BlogPost, slug=slug)
    if user != blog.user:
        messages.error(self.request, "Permission Denied: You cannot delete anyone else's post.")
        return redirect(reverse('user-profile', kwargs={'username':user.username}))

    if blog is not None:
        blog.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect(reverse('user-profile', kwargs={'username':user.username}))

    return redirect(reverse('user-profile', kwargs={'username':user.username}))


"""
Post likes.
=======================================
"""
from django.http import JsonResponse

# @login_required(login_url='/accounts/login/')
def like_blog_post(request, slug):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({
            'url': reverse('user-login'),
            'result': 'user-not-authenticated'
        })

    if request.is_ajax() and request.method == 'POST':
        blog = get_object_or_404(BlogPost, slug=slug)
        if blog not in user.userprofile.liked_posts.all():
            blog.likes = blog.likes + 1
            blog.save()
            user.userprofile.liked_posts.add(blog)
            return JsonResponse({
                "likes": blog.likes,
                "post_liked": True 
            })
        else:
            if blog.likes > 0:
                blog.likes = blog.likes - 1
                blog.save()
            user.userprofile.liked_posts.remove(blog)
            return JsonResponse({
                "likes": blog.likes,
                "post_liked": False
            })
    else:
        print('not ajax')