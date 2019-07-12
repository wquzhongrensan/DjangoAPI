from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

# 会员等级
member_level_choice = (
        ('general', '普通用户'),
        ('VIP', 'VIP会员'),
        ('gold', '铂金会员'),
        ('other', '其他')
    )

gender = (
    ('male', "男"),
    ('female', "女"),
    ("secret", u"保密")
)

#  壹言的用户模型
# django自带的user model只有下面这些字段 9个字段
# username：用户名
# email: 电子邮件
# password：密码
# first_name：名
# last_name：姓
# is_active: 是否为活跃用户。默认是True
# is_staff: 是否为员工。默认是False
# is_superuser: 是否为管理员。默认是False
# date_joined: 加入日期。系统自动生成。
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True)
    sign = models.CharField(max_length=200, null=True, verbose_name="用户签名")

    #  目前会员分为： 1.普通用户  2.vip账号  3.铂金账号 (其他等级)
    memberLevel = models.CharField(verbose_name=u'会员等级', max_length=32,
                                       choices=member_level_choice, blank=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}".format(self.user.__str__())


# 继承AbstractUser实现
# class UserProfile(AbstractUser):
#
#     """ 用户 """
#     name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
#     birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
#     gender = models.CharField(max_length=6, choices=gender)
#     mobile = models.CharField(max_length=11, verbose_name="电话")
#     email = models.EmailField(max_length=100, null=True, verbose_name="邮箱")
#     other = models.CharField(max_length=50, null=True, verbose_name="其他扩展信息")
#     isVip = models.CharField(max_length=1, null=True, verbose_name="是否是VIP会员")
#     #  目前会员分为： 1.普通用户  2.vip账号  3.铂金账号 (其他等级)
#     memberLevel = models.CharField(verbose_name=u'会员等级', max_length=32,
#                                    choices=member_level_choice, blank=True)
#
#     class Meta:
#         verbose_name = "用户"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name



# 扩展系统自带user 方式实现自定义user模型
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.__str__()



#  关注表
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follower', on_delete=models.CASCADE)
    # on_delete是 Django2必须要的 Django2.0必须的
    followed = models.ForeignKey(UserProfile, related_name='followed', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    # 关注某人
    @staticmethod
    def follow(from_user, to_user):
        Follow(follower=from_user,
               followed=to_user).save()  # 关注方法

    # 取消关注某人
    @staticmethod
    def unfollow(from_user, to_user):
        f = Follow.objects.filter(follower=from_user, followed=to_user).all()
        if f:
            f.delete()  # 取关

    # 用户的所有关注的人
    @staticmethod
    def user_followed(from_user):
        followeders = Follow.objects.filter(follower=from_user).all()
        user_followed = []
        for followeder in followeders:
            user_followed.append(followeder.followed)
        return user_followed  # 得到from_user关注的人，返回列表

    # 按插入日期的倒叙排序
    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.follower} follow {self.followed}'


# class Article(models.Model):
#
#     title = models.CharField('标题', max_length=70)
#     keywords = models.CharField('文章关键词', max_length=120, blank=True, null=True)
#     excerpt = models.TextField('摘要', max_length=200, blank=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', blank=True, null=True)
#     body = models.TextField('内容')
#     user = models.ForeignKey(Userinfo, on_delete=models.CASCADE, verbose_name='作者')
#     views = models.PositiveIntegerField('阅读量', default=0)
#     top = models.IntegerField(choices=[(0, '否'), (1, '是'), ], default=0, verbose_name='是否推荐')
#     created_time = models.DateTimeField('发布时间', auto_now_add=True)
#     modified_time = models.DateTimeField('修改时间', auto_now=True)
#
#     class Meta:
#         verbose_name = '文章'
#         verbose_name_plural = '文章'
#
#     def __str__(self):
#         return self.title