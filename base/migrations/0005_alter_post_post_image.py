# Generated by Django 5.0.2 on 2024-04-10 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_post_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(default=None, max_length=250, null=True, upload_to='images/'),
        ),
    ]