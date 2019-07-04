from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.

class TestModel(models.Model):
    name = models.CharField(u'姓名', max_length=100, default='no_name')
    sex = models.CharField(u'性别', max_length=10, default='male')
    age = models.CharField(u'年龄', max_length=3, default='0')

    def __str__(self):
        return '%d: %s' % (self.pk, self.name)


# 示范 snippet 和 group 的区别
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    # language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    # style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    # 意思是 这个 snippet地属于那一个group
    group = models.ForeignKey('Group', related_name='snippet', null=True, on_delete=models.CASCADE)  #建立外键，一定要写上related_name

    class Meta:
        ordering = ('created',)


# 出来的结果怎么是反向的
class Group(models.Model):
    class_room = models.CharField(max_length=50)
    number = models.IntegerField()

    class Meta:
        db_table = 'group'

# 演示使用 Django自定义接口  而不使用Django rest framework
class Questionnaire(models.Model):
    '''问卷'''
    title = models.CharField('标题', max_length=100)

    class Meta:
        verbose_name_plural = '所有问卷'

    def questionnaire_to_dict(self):
        '''把questionnaire对象转化为字典'''
        return dict(questionnaire_id=self.id, title=self.title,
                    questions=[question.question_to_dict() for question in self.questions.all()])

    def __str__(self):
        return self.title


class Question(models.Model):
    '''问题'''
    # 所属问卷
    questionnaire = models.ForeignKey(Questionnaire, verbose_name='所属问卷', related_name='questions', on_delete=models.CASCADE)
    # 问题标题
    title = models.CharField('问题', max_length=150)
    # 是否是多选
    is_checkbox = models.BooleanField('是否多选', default=False, help_text='是否是多选问题')

    class Meta:
        verbose_name_plural = '问题'

    def question_to_dict(self):
        '''把question对象转化为字典'''
        return dict(title=self.title, choice=[choice.choice_to_dict() for choice in self.choices.all()],
                    is_checkbox=self.is_checkbox, questionnaire_id=self.questionnaire.id)

    def __str__(self):
        return self.title


class Choice(models.Model):
    '''选项'''
    # 所属的问题
    question = models.ForeignKey(Question, verbose_name='所属问题', related_name='choices', on_delete=models.CASCADE)
    content = models.CharField('选项内容', max_length=150)

    class Meta:
        verbose_name_plural = '问题选项'

    def choice_to_dict(self):
        '''把choice对象转化为字典'''
        # 选项id,选项所属的问题id,选项内容
        return dict(id=self.id, question_id=self.question.id, content=self.content)

    def __str__(self):
        return self.content

# class UserProfile(AbstractUser):
#     """ 用户 """
#     name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
#     birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
#     gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", u"女")))
#     mobile = models.CharField(max_length=11, verbose_name="电话")
#     email = models.EmailField(max_length=100, null=True, verbose_name="邮箱")
#     other = models.CharField(max_length=50, null=True, verbose_name="其他扩展信息")
#     class Meta:
#         verbose_name = "用户"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.username
#
# class VerifyCode(models.Model):
#     """ 短信验证码 """
#     code = models.CharField(max_length=10, verbose_name="验证码")
#     mobile = models.CharField(max_length=11, verbose_name="电话")
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = "短信验证码"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.code


class Region(models.Model):
    """
    区域
    """
    region_name = models.CharField(verbose_name=u'区域', max_length=64, blank=True, unique=True)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField(verbose_name=u'修改时间', null=True)
    is_delete = models.IntegerField(u'删除', default=0)

    class Meta:
        verbose_name = u'区域'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.region_name


class MachineRoom(models.Model):
    """
    机房
    """
    room_name = models.CharField(verbose_name=u'机房名称', max_length=64, blank=True, unique=True)
    room_code = models.CharField(verbose_name=u'机房编号', max_length=64, blank=True, null=True)
    region_id = models.IntegerField(verbose_name=u'区域id', blank=True)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField(verbose_name=u'修改时间', null=True)
    is_delete = models.IntegerField(u'删除', default=0)

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.room_name


class Cabinet(models.Model):
    """
    机柜
    """
    cabinet_name = models.CharField(verbose_name=u'机柜名称', max_length=64, blank=True)
    cabinet_code = models.CharField(verbose_name=u'机柜编号', max_length=64, blank=True)
    room_id = models.IntegerField(verbose_name=u'机房id', blank=True)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField(verbose_name=u'修改时间', null=True)
    is_delete = models.IntegerField(u'删除', default=0)

    class Meta:
        verbose_name = u'机柜'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cabinet_name


class Device(models.Model):
    """
    设备
    """
    type_choices = (
        ('storage', '存储设备'),
        ('safe', '安全设备')
    )

    device_name = models.CharField(verbose_name=u'设备名称', max_length=64,
                                   blank=True, unique=True)
    device_type = models.CharField(verbose_name=u'设备类型', max_length=32,
                                   choices=type_choices, blank=True)
    brand = models.CharField(verbose_name=u'品牌', max_length=32, blank=True, null=True)
    model = models.CharField(verbose_name=u'型号', max_length=32, blank=True, null=True)
    hardware = models.TextField(verbose_name=u'硬件信息', blank=True, null=True)
    cabinet_id = models.IntegerField(verbose_name=u'机柜id', blank=True)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, null=True)
    modified_time = models.DateTimeField(verbose_name=u'修改时间', null=True)
    is_delete = models.IntegerField(u'删除', default=0)

    class Meta:
        verbose_name = u'设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device_name


class Server(models.Model):
    """
    物理服务器
    """
    status_choice = (
        ('online', '上线'),
        ('offline', '下线'),
        ('normal', '正常'),
        ('abnormal', '异常')
    )

    server_name = models.CharField(verbose_name=u'服务器名称', max_length=128, blank=False, null=False)
    server_num = models.CharField(verbose_name=u'服务器编号', max_length=128, blank=True, null=True)
    brand = models.CharField(verbose_name=u'品牌', max_length=64, blank=True, null=True)
    model = models.CharField(verbose_name=u'型号', max_length=64, blank=True, null=True)
    cpus = models.IntegerField(verbose_name=u'cpu核数', default=0)
    ram = models.IntegerField(verbose_name=u'内存大小', default=0)
    disk = models.IntegerField(verbose_name=u'磁盘大小', default=0)
    product_date = models.DateTimeField(verbose_name=u'生产日期', auto_now_add=True)
    status = models.CharField(verbose_name=u'状态', max_length=16, choices=status_choice)

    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name=u'修改时间', auto_now_add=True)

    class Meta:
        verbose_name = u'服务器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.server_name

