# Generated by Django 5.0.1 on 2024-02-26 16:54

import markdownx.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_options_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=markdownx.models.MarkdownxField(blank=True, verbose_name='本文'),
        ),
    ]
