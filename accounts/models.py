from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from blogpost.models import BlogPost
from replies.models import Reply

# Create your models here.
User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        'self', related_name="followed_by", blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        upload_to='images/profile-image/%Y/%m/%d/', null=True, blank=True)
    liked_posts = models.ManyToManyField(BlogPost, blank=True)
    liked_replies = models.ManyToManyField(Reply, blank=True)

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'username': self.user.username})

    def get_all_followings(self):
        return self.following.all()

    def get_profile_image_url(self):
        img = self.profile_image
        dummy_url = 'https://i.pravatar.cc/300?u={username}'.format(
            username=self.user.username)
        if img and img.url != '/media/False':
            return img.url
        return dummy_url


"""
When an user is saved its profile must be created.
A post_save is used for creating a profile.
"""


def user_profile_create_reviever(sender, instance, created, *args, **kwargs):
    if created:
        try:
            user, user_created = UserProfile.objects.get_or_create(
                user=instance)
        except:
            print('Error in profile creation.')


post_save.connect(user_profile_create_reviever, sender=User)
"""
End.
"""

"""
---When followers is changed the following of the follower must be changed.
---But it didn't worked.😁

def following_changed_reciever(sender, instance, action, *args, **kwargs):
    print(action)
    if action == "pre_add" or action == "post_add":
        all_followings = instance.following.all()
        for user in all_followings:
            user.followers.add(instance)
            print(user, "following", user.followers.all())
            user.save()

    if action == "pre_remove" or action == "post_remove":
        all_followings = instance.following.all()
        for user in all_followings:
            user.followers.remove(instance)
            print(user, "following", user.followers.all())
            user.save()

m2m_changed.connect(following_changed_reciever, sender=UserProfile.following.through)
"""
