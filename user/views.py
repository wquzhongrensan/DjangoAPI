from django.shortcuts import render
from .models import Follow, UserProfile


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
