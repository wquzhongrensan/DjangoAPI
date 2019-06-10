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

