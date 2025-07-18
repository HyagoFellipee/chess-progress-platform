from django.db import models
from django.contrib.auth.models import User
import uuid

class ChessAnalysis(models.Model):
    """Model to store chess evolution analyses"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    GAME_MODE_CHOICES = [
        ('blitz', 'Blitz'),
        ('rapid', 'Rapid'),
        ('bullet', 'Bullet'),
        ('daily', 'Daily'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chess_analyses')
    
    # Input parameters
    chess_username = models.CharField(max_length=100)
    end_date = models.DateField()
    game_mode = models.CharField(max_length=10, choices=GAME_MODE_CHOICES)
    
    # Analysis status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    celery_task_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Results
    user_current_rating = models.IntegerField(blank=True, null=True)
    user_position_in_ranking = models.IntegerField(blank=True, null=True)
    total_opponents = models.IntegerField(blank=True, null=True)
    percentile = models.FloatField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    
    # Payment info
    is_paid = models.BooleanField(default=False)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chess Analysis'
        verbose_name_plural = 'Chess Analyses'
    
    def __str__(self):
        return f"{self.chess_username} - {self.game_mode} - {self.status}"


class OpponentRating(models.Model):
    """Model to store opponent ratings"""
    
    analysis = models.ForeignKey(ChessAnalysis, on_delete=models.CASCADE, related_name='opponent_ratings')
    opponent_username = models.CharField(max_length=100)
    current_rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['analysis', 'opponent_username']
        verbose_name = 'Opponent Rating'
        verbose_name_plural = 'Opponent Ratings'
    
    def __str__(self):
        return f"{self.opponent_username}: {self.current_rating}"


class AnalysisCache(models.Model):
    """Cache for opponent ratings to optimize repeated requests"""
    
    username = models.CharField(max_length=100)
    game_mode = models.CharField(max_length=10, choices=ChessAnalysis.GAME_MODE_CHOICES)
    rating = models.IntegerField()
    cached_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['username', 'game_mode']
        verbose_name = 'Analysis Cache'
        verbose_name_plural = 'Analysis Caches'
    
    def __str__(self):
        return f"{self.username} ({self.game_mode}): {self.rating}"
