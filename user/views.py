from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# 获取用户信息
@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    # 查询到用户信息
    return render(request, 'users/profile.html', {'user': user})

# 用户信息更新
@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)

    return render(request, 'users/profile_update.html', {'form': form, 'user': user})



# 获取所有关注者的文章列表 分也返回
def followed(request):
    user = request.user
    all_feeds = Feed.get_feeds().filter(user__in=Follow.user_followed(user))
    #user__in 表示查询在给定的列表中
    paginator = Paginator(all_feeds, FEEDS_NUM_PATES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'feeds/followed_feeds.html', {
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1,
    })


# # 注册功能
# def register(request):
#     if request.method == 'POST':
#
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password2']
#
#             # 使用内置User自带create_user方法创建用户，不需要使用save()
#               user = User.objects.create_user(username=username, password=password, email=email)
#
#             # 如果直接使用objects.create()方法后不需要使用save()
#               user_profile = UserProfile(user=user)
#             user_profile.save()
#
#             return HttpResponseRedirect("/accounts/login/")
#
#     else:
#         form = RegistrationForm()
#
#     return render(request, 'users/registration.html', {'form': form})
#
#
# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#            username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             user = auth.authenticate(username=username, password=password)
#
#             if user is not None and user.is_active:
#                auth.login(request, user)
#                return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
#
#             else:
#                 # 登陆失败
#                  return render(request, 'users/login.html', {'form': form,
#                                'message': 'Wrong password. Please try again.'})
#     else:
#         form = LoginForm()
#
#     return render(request, 'users/login.html', {'form': form})
