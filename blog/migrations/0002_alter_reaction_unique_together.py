# Generated by Django 4.2.3 on 2023-07-19 02:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together={('comment', 'user', 'reaction_type'), ('post', 'user', 'reaction_type')},
        ),
    ]