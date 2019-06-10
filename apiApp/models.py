from django.db import models

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
    number = models.IntegerField(max_length=10)

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

