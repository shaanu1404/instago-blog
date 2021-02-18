from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout, decorators
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, ListView
from django.urls import reverse
from django.db.models import Q

from accounts.models import UserProfile
from .forms import RegistrationForm, LoginAuthForm, UserProfileUpdateForm, UserUpdateForm

# Create your views here.
def follow(request):
    user_id = request.POST.get('userid')
    user_profile = get_object_or_404(UserProfile, user=user_id)
    curr_user = request.user

    if user_profile not in curr_user.userprofile.get_all_followings():
        curr_user.userprofile.following.add(user_profile)

    page_redirect_url = request.POST.get('pageredirect')
    if page_redirect_url:
        return redirect(page_redirect_url)

    blog_id = request.POST.get('blogid')
    if blog_id:
        curr_page = request.POST.get('page', 1)
        return redirect(reverse('home') + '?page={curr_page}#blog-{blog_id}'.format(curr_page=curr_page, blog_id=blog_id))

    return redirect(reverse('home'))

def unfollow(request):
    user_id = request.POST.get('userid')
    user_profile = get_object_or_404(UserProfile, user=user_id)
    curr_user = request.user

    if user_profile in curr_user.userprofile.get_all_followings():
        curr_user.userprofile.following.remove(user_profile)

    page_redirect_url = request.POST.get('pageredirect')
    if page_redirect_url:
        return redirect(page_redirect_url)

    blog_id = request.POST.get('blogid')
    if blog_id:
        curr_page = request.POST.get('page', 1)
        return redirect(reverse('home') + '?page={curr_page}#blog-{blog_id}'.format(curr_page=curr_page, blog_id=blog_id))

    return redirect(reverse('home'))

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
class UserDetails(DetailView):
    template_name = "accounts/profile.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    """ Get context data.    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context['object']
        blogs = object.blogpost_set.all().order_by('-timestamp')
        paginator = Paginator(blogs, 3)
        page = self.request.GET.get('page', None)
        paged_blogs = paginator.get_page(page)
        context['blogs'] = paged_blogs
        return context


    """ Get slug field.
    def get_slug_field(self, **kwargs):
        slug = super().get_slug_field(**kwargs)
        return slug
    """


def register_user(request):

    if request.user.is_authenticated:
        return redirect('/')

    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "You are registered successfully. Welcome to our community. Please Login.")
            form = RegistrationForm(None)
            return redirect(reverse('user-login'))

    context = {
        "form" : form
    }
    return render(request, 'accounts/user_registration.html', context)

class AccountsLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/user_login.html'
    form_class = LoginAuthForm
    redirect_authenticated_user = True
    # success_message = "You're welcome."

    def get_success_message(self, cleaned_data):
        username = cleaned_data['username']
        user = User.objects.get(username=username)
        return f"{user.get_full_name()}, Welcome to InstaGo."

    def form_invalid(self, form):
        messages.error(self.request, 'Please insert a valid username or password.')
        return self.render_to_response(self.get_context_data(form=form))

    # def get_context_data(self, *args, **kwargs):
    #     context = super(AccountsLoginView, self).get_context_data(*args, **kwargs)
    #     return context


def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out successfully.')
    return redirect(reverse('user-login'))



"""
Profile updation goes here.
=========================================
"""
@decorators.login_required(login_url='/accounts/login/')
def user_profile_update(request):
    user = request.user

    user_form = UserUpdateForm(
        request.POST or None,
        request.FILES or None,
        initial={
            'first_name' : user.first_name,
            'last_name' : user.last_name,
        }
    )
    profile_form = UserProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        initial={
            'bio' : user.userprofile.bio,
            'profile_image' : user.userprofile.profile_image,
        }
    )

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()

            profile = UserProfile.objects.get(user=user)
            profile.bio = profile_form.cleaned_data['bio']
            profile.profile_image = profile_form.cleaned_data['profile_image']
            profile.save()

            messages.success(request, 'Profile saved successfully.')
            return redirect(profile.get_absolute_url())

        else:
            messages.error(request, "Invalid input.")


    context = {
        "profile_form" : profile_form,
        "user_form" : user_form
    }
    return render(request, 'accounts/user_update.html' , context)



"""
Profile search goes here.
=========================================
"""
class UsersListView(ListView):
    model = User
    template_name = 'accounts/list.html'
    # paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        obj_list = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            obj_list = obj_list.exclude(username=user.username).order_by('first_name')

        q = self.request.GET.get('q', None)
        if q is not None:
            lookup = (Q(username__icontains=q) |
                        Q(first_name__startswith=q) | 
                        Q(last_name__startswith=q) |
                        Q(email__icontains=q)
                        )
            obj_list = obj_list.filter(lookup).distinct()
        return obj_list


@decorators.login_required(login_url='/accounts/login/')
def edit_bio(request):
    user = request.user
    if request.method == 'POST':
        bio = request.POST.get('bio', None)
        if bio is not None:
            user_profile = user.userprofile
            user_profile.bio = bio
            user_profile.save()
            messages.success(request, 'Bio updated.')
            return redirect(reverse('user-profile', kwargs={'username': user.username}))

