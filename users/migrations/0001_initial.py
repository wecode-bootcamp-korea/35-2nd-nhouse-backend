# Generated by Django 4.0.6 on 2022-08-02 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'follows',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.CharField(max_length=200, unique=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('nickname', models.CharField(max_length=50, null=True)),
                ('profile_image', models.URLField(max_length=300, null=True)),
                ('follow', models.ManyToManyField(through='users.Follow', to='users.user')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='follow',
            name='following_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='users.user'),
        ),
        migrations.AddField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='users.user'),
        ),
    ]
