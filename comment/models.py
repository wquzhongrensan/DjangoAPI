from django.db import models
from apiApp.models import Server
# Create your models here.
# 对于每一个句子的评论
class Comment(models.Model):
    """
    一条评论 可以是对 句子评论 也可以是对已有评论的评论
    """
    status_choice = (
        ('online', '上线'),
        ('offline', '下线'),
        ('normal', '正常'),
        ('abnormal', '异常')
    )

    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=300)

    in_post = models.ForeignKey(Server, related_name='comments', on_delete=models.CASCADE)
    reply_comment = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('-pub_time',)
        verbose_name = u'句子评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.body