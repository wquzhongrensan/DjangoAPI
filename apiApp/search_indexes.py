from haystack import indexes
from .models import *


# 这里  类名是 模型类名称+Index
class ServerIndex(indexes.SearchIndex, indexes.Indexable):
    # 指定模型类那个字段 建立 索引 ， 后面还会有一个模版文件
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Server


    def index_queryset(self, using=None):
        return self.get_model().objects.all()