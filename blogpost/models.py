from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django_quill.fields import QuillField

from blog.utils import unique_slug_generator

User = get_user_model()

class BlogPost(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, blank=True, null=True)
    body = models.TextField()
    content = QuillField(default="", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='images/cover-image/%Y/%m/%d/', null=True, blank=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={ "slug" : self.slug })

    def get_profile_image_url(self):
        return self.user.userprofile.get_profile_image_url()

    def get_all_tags(self):
        tags = self.tag_set.all()
        data = []
        for tag in tags:
            hashtag = "#" + "".join(tag.title.split())
            data.append(hashtag)
        return data


def blog_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(blog_pre_save_reciever, sender=BlogPost)
