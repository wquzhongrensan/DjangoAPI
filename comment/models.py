from django.db import models

class Post(models.Model):
    """
    文章的存储model
    """

    """
    title:标题
    body:主体
    pub_time:发布时间
    tag:标签,多对多
    author:作者,一对多
    """
    title = models.CharField(max_length=100, blank=True, default="")
    body = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_time',)

    # 文章摘要
    def excerpt(self):
        excerpt = str(self.body)
        if excerpt.__len__() > 50:
            # 取前面的50个字 加上 省略号
            excerpt = excerpt[:50]+'...'
        return excerpt


class Tag(models.Model):
    # 标签的名字
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Comment(models.Model):
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=300)
    # 是对那篇文章的评论
    in_post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    # 是对那条评论的回复评论
    reply_comment = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        # 按发布时间的倒序排
        ordering = ('-pub_time',)
