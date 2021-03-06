# Generated by Django 2.2.2 on 2019-06-10 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0002_group_snippet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
            ],
            options={
                'verbose_name_plural': '所有问卷',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='问题')),
                ('is_checkbox', models.BooleanField(default=False, help_text='是否是多选问题', verbose_name='是否多选')),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='apiApp.Questionnaire', verbose_name='所属问卷')),
            ],
            options={
                'verbose_name_plural': '问题',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=150, verbose_name='选项内容')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='apiApp.Question', verbose_name='所属问题')),
            ],
            options={
                'verbose_name_plural': '问题选项',
            },
        ),
    ]
