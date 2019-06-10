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
        fields = ('title',)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'is_checkbox', 'questionnaire')


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('content', 'question')

