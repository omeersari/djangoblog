# Generated by Django 3.0.7 on 2020-06-12 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='status',
            new_name='blog_status',
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.TextField()),
                ('comment_published', models.DateTimeField(auto_now_add=True)),
                ('comment_status', models.CharField(choices=[('published', 'Yayınlandı'), ('deleted', 'Silindi')], default='published', max_length=10)),
                ('comment_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL)),
                ('comment_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Blog')),
            ],
            options={
                'ordering': ['comment_published'],
            },
        ),
    ]
