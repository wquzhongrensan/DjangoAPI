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
    update_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    # 是否允许评论
    allow_comments = models.BooleanField(verbose_name="允许评论", default=True)
    # 点赞数目
    vote_num = models.IntegerField(verbose_name="点赞数量", default=0)

    # 新添views字段记录阅读量 文章阅读数
    # views = models.PositiveInterField(default=0)

    class Meta:
        ordering = ('-pub_time',)

    # 文章摘要
    def excerpt(self):
        excerpt = str(self.body)
        if excerpt.__len__() > 50:
            # 取前面的50个字 加上 省略号
            excerpt = excerpt[:50]+'...'
        return excerpt

        # ... 其它已有的模型方法
    # 有用户访问了某个文章 就对应将views+1
    def increase_views(self):
        self.views += 1
        # update_fields 只是告诉数据库只是更新views字段，提高效率
        # 多人同时访问导致的误差是可以忽略不计的
        self.save(update_fields=['views'])

    def articlecont(request):
        # 文档内容
        # 获取显示的文章id
        nid = request.GET.get('nid')
        # 获取文章
        articledata = models.article.objects.filter(id=nid).first()
        # 获取到的文章调用incease_views方法
        models.article.increase_views(articledata)
        # 根据自增的views字段进行排序，并获取最高的5条数据
        hotdoc = models.article.objects.order_by("-views")[0:5]
        return render(request, "articlecont.html", {"articledata": articledata, 'hotdoc': hotdoc})


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
