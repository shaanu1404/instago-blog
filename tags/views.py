from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import auth, messages

from .models import Tag
from .forms import AddTagForm
from blogpost.models import BlogPost

@auth.decorators.login_required(login_url="/accounts/login/")
def add_tags(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    form = AddTagForm(request.POST or None, initial={ "tags": blog.tag_set.all() })

    if request.user != blog.user:
        messages.error(request, 'You cannot edit someone else\'s post.')
        return redirect(reverse('user-profile', kwargs={ 'username' : blog.user.username }))

    if request.method == 'POST':
        if form.is_valid():
            tags = form.cleaned_data['tags']
            blog.tag_set.add(*tags)
            messages.success(request, 'Tags updated.')
            return redirect(reverse('detail', kwargs={ 'slug':blog.slug }))
        else:
            messages.error(request, 'Invalid data.')
            return redirect(reverse('user-profile', kwargs={ 'username' : blog.user.username }))

    context = {
        "blog": blog,
        "form": form
    }
    return render(request, 'tags/add_tags.html', context)


@auth.decorators.login_required(login_url="/accounts/login/")
def create_new_tag(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        blog_slug = request.POST.get('blogslug', None)
        if title is not None:
            Tag.objects.create(title=title)
            messages.success(request, 'New tag created.')
            return redirect(reverse('add-tag', kwargs={ 'slug': blog_slug }))
        else:
            messages.error(request, 'Error occurred.')
            return redirect(reverse('add-tag', kwargs={ 'slug': blog_slug }))
    else:
        pass