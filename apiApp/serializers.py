from rest_framework import serializers
from apiApp.models import TestModel, Snippet, Group, Question, Questionnaire, Choice

class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel  # 序列化的对象
        fields = ('name', 'sex', 'age',)  # 需要序列化的属性

class SnippetSerializers(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        fields = '__all__'


class GroupSerializers(serializers.ModelSerializer):
    snippet = SnippetSerializers(read_only=True, many=True)  #外键的related_name，many=True不能缺少

    class Meta:
        model = Group
        fields = '__all__'


#  使用Django rest framework 的方式实现同样的功能
class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ('title',) # 序列化哪些字段


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'is_checkbox', 'questionnaire')


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('content', 'question')


# serializer有三个功能： 1.对象转json   2.验证用户提交的数据  3.在返回给客户端的数据中返回URL
# 使用serializer 来验证 客户端提交的数据 演示
# class UserModelSerializer(serializers.ModelSerializer):
#     # ModelSerializer继承于Serializer,所以在里面Serializers中的语法仍然是可以使用的
#     user_type = serializers.CharField(source='get_user_type_display')
#     group = serializers.CharField(source='group.title')
#     role = serializers.SerializerMethodField()
#
#     # get_字段名称；自定义显示字段实现需要定义这样的一个方法
#     def get_role(self, obj):
#         # obj就是UserInfo的对象  user.role.all()  /  role.user_set.all()
#         roles = obj.role.all()
#         results = []
#         for role in roles:
#             results.append({
#                 'id': role.id,
#                 'title': role.title
#             })
#         return results
#
#     class Meta:
#         # 指定要序列化哪一个模型
#         model = UserInfo
#         # ModelSerializer类使用fields控制需要序列化的字段
#         # fields = "__all__"
#         fields = ('role','group','user_type','username')

