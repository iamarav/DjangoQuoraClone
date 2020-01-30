# Generated by Django 3.0.2 on 2020-01-23 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Questions', '0005_questions_anonymous'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Question Category',
                'verbose_name_plural': 'Question Categories',
            },
        ),
        migrations.AddField(
            model_name='questions',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='Questions.QuestionCategory'),
            preserve_default=False,
        ),
    ]
