from django.contrib import admin
from .models import ChessAnalysis, OpponentRating, AnalysisCache

@admin.register(ChessAnalysis)
class ChessAnalysisAdmin(admin.ModelAdmin):
    list_display = ['chess_username', 'game_mode', 'status', 'user', 'created_at', 'is_paid']
    list_filter = ['status', 'game_mode', 'is_paid', 'created_at']
    search_fields = ['chess_username', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'chess_username', 'game_mode', 'end_date')
        }),
        ('Status', {
            'fields': ('status', 'celery_task_id', 'error_message')
        }),
        ('Results', {
            'fields': ('user_current_rating', 'user_position_in_ranking', 'total_opponents', 'percentile')
        }),
        ('Payment', {
            'fields': ('is_paid', 'stripe_payment_intent_id')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OpponentRating)
class OpponentRatingAdmin(admin.ModelAdmin):
    list_display = ['opponent_username', 'current_rating', 'analysis', 'created_at']
    list_filter = ['created_at']
    search_fields = ['opponent_username', 'analysis__chess_username']

@admin.register(AnalysisCache)
class AnalysisCacheAdmin(admin.ModelAdmin):
    list_display = ['username', 'game_mode', 'rating', 'cached_at']
    list_filter = ['game_mode', 'cached_at']
    search_fields = ['username']
