# Generated by Django 2.0.3 on 2018-03-25 10:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Name')),
                ('info', models.CharField(blank=True, max_length=200, null=True, verbose_name='Short Info')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='static/profile_pics/%Y-%m-%d/', verbose_name='Group picture')),
                ('admin', models.ManyToManyField(related_name='group_admin', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='group_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]