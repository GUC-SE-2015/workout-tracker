# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('commenter', models.ForeignKey(related_name='commenter', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=1, choices=[(b'F', b'Female'), (b'M', b'Male')])),
                ('myImg', models.ImageField(upload_to=b'images/', null=True, verbose_name=b'Profile Pic', blank=True)),
                ('type', models.CharField(max_length=256, choices=[(b'trainer', b'trainer'), (b'client', b'client')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('userinfo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='workout_tracker.UserInfo')),
                ('phone', models.CharField(max_length=30)),
                ('experience', models.TextField()),
                ('education', models.TextField()),
            ],
            options={
            },
            bases=('workout_tracker.userinfo',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('userinfo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='workout_tracker.UserInfo')),
                ('health_issues', models.TextField()),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('trainer', models.ForeignKey(related_name='clients', blank=True, to='workout_tracker.Trainer', null=True)),
            ],
            options={
            },
            bases=('workout_tracker.userinfo',),
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workout', models.TextField()),
                ('date_posted', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('client', models.ForeignKey(related_name='workout', blank=True, to='workout_tracker.Client', null=True)),
                ('posted_by', models.ForeignKey(related_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(related_name='user_info', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
