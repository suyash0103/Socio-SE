# Generated by Django 2.0.3 on 2019-03-30 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_face_face_encoding'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='face_encoding',
            field=models.BinaryField(null=True),
        ),
    ]
