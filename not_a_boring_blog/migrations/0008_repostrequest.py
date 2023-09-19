# Generated by Django 4.2.4 on 2023-09-15 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('not_a_boring_blog', '0007_alter_comment_options_alter_comment_parent_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepostRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('approve', 'Approved'), ('denied', 'Denied')], max_length=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repost', to='not_a_boring_blog.post')),
                ('requester_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='not_a_boring_blog.role')),
            ],
        ),
    ]