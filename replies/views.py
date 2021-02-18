from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User

from blogpost.models import BlogPost
from .models import Reply

# Create your views here.
def comment(request, blog_id, user_id):
    if request.method == 'POST':
        user_reply = request.POST.get('reply', None)
        if not user_reply:
            raise ValueError('Reply must not be empty.')

        blog = get_object_or_404(BlogPost, id=blog_id)
        user = get_object_or_404(User, id=user_id)
        reply = Reply(reply=user_reply)
        reply.post = blog
        reply.user = user
        reply.save()

    return redirect(reverse('detail', kwargs={ "slug" : blog.slug }) + '#comments')

# @login_required(login_url='/accounts/login/')
def like_reply(request, id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({
            'url': reverse('user-login'),
            'result': 'user-not-authenticated'
        })

    if request.is_ajax() and request.method == 'POST':
        reply = get_object_or_404(Reply, id=id)
        if reply not in user.userprofile.liked_replies.all():
            reply.likes = reply.likes + 1
            reply.save()
            user.userprofile.liked_replies.add(reply)
            return JsonResponse({
                "likes": reply.likes,
                "reply_liked": True 
            })
        else:
            if reply.likes > 0:
                reply.likes = reply.likes - 1
                reply.save()
            user.userprofile.liked_replies.remove(reply)
            return JsonResponse({
                "likes": reply.likes,
                "reply_liked": False
            })
    else:
        print('not ajax')