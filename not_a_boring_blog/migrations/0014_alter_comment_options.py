# Generated by Django 4.2.4 on 2023-09-20 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('not_a_boring_blog', '0013_alter_repostrequest_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
    ]
