# Generated by Django 5.2.4 on 2025-07-18 15:30

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('game_mode', models.CharField(choices=[('blitz', 'Blitz'), ('rapid', 'Rapid'), ('bullet', 'Bullet'), ('daily', 'Daily')], max_length=10)),
                ('rating', models.IntegerField()),
                ('cached_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Analysis Cache',
                'verbose_name_plural': 'Analysis Caches',
                'unique_together': {('username', 'game_mode')},
            },
        ),
        migrations.CreateModel(
            name='ChessAnalysis',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('chess_username', models.CharField(max_length=100)),
                ('end_date', models.DateField()),
                ('game_mode', models.CharField(choices=[('blitz', 'Blitz'), ('rapid', 'Rapid'), ('bullet', 'Bullet'), ('daily', 'Daily')], max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('celery_task_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user_current_rating', models.IntegerField(blank=True, null=True)),
                ('user_position_in_ranking', models.IntegerField(blank=True, null=True)),
                ('total_opponents', models.IntegerField(blank=True, null=True)),
                ('percentile', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('stripe_payment_intent_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chess_analyses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Chess Analysis',
                'verbose_name_plural': 'Chess Analyses',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OpponentRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opponent_username', models.CharField(max_length=100)),
                ('current_rating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_ratings', to='analysis.chessanalysis')),
            ],
            options={
                'verbose_name': 'Opponent Rating',
                'verbose_name_plural': 'Opponent Ratings',
                'unique_together': {('analysis', 'opponent_username')},
            },
        ),
    ]
