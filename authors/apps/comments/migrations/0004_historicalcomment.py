# Generated by Django 2.1.5 on 2019-01-29 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20190125_1512'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0006_article_tags'),
        ('comments', '0003_merge_20190129_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalComment',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('body', models.TextField(max_length=500)),
                ('createdAt', models.DateTimeField(blank=True, editable=False)),
                ('updatedAt', models.DateTimeField(blank=True, editable=False)),
                ('highlight_start', models.PositiveIntegerField(blank=True, null=True)),
                ('highlight_end', models.PositiveIntegerField(blank=True, null=True)),
                ('highlight_text', models.TextField(max_length=500, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('article', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='articles.Article')),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='profiles.Profile')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical comment',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]