# Generated by Django 3.0.4 on 2020-07-31 16:21

import chart.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Track title')),
                ('slug', models.SlugField(blank=True, help_text='Click on the title field to populate this field', max_length=200, null=True, unique=True)),
                ('artist', models.CharField(max_length=150)),
                ('link', models.CharField(blank=True, help_text='Optional', max_length=200, null=True, verbose_name='Song Link')),
                ('description', models.TextField(blank=True, help_text='Optional', max_length=225, null=True, verbose_name='Song Description')),
                ('artwork', models.ImageField(default='artwork/default.jpg', upload_to='artwork')),
                ('zgm_rank', models.IntegerField(blank=True, null=True, unique=True, verbose_name='ZGM Rank')),
                ('uni_rank', models.IntegerField(blank=True, null=True, verbose_name='University Rank')),
                ('released', models.DateField(default=chart.models.today_utc)),
                ('submission', models.IntegerField(choices=[(0, 'In Review'), (1, 'Accepted'), (2, 'Denied')], default=0, verbose_name='Submission Status')),
                ('status', models.IntegerField(choices=[(0, 'Not Charting'), (1, 'Charting')], default=0, verbose_name='Chart Status')),
                ('artist_tag', models.ManyToManyField(blank=True, help_text='Optional:Tag artist and producers', related_name='artists', to='artist.Artist', verbose_name='Artist Tag')),
            ],
            options={
                'ordering': ['-released'],
            },
        ),
    ]
