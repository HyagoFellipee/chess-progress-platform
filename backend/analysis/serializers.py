from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChessAnalysis, OpponentRating, AnalysisCache

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class OpponentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpponentRating
        fields = ['opponent_username', 'current_rating', 'created_at']

class ChessAnalysisSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    opponent_ratings = OpponentRatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChessAnalysis
        fields = [
            'id', 'user', 'chess_username', 'end_date', 'game_mode',
            'status', 'user_current_rating', 'user_position_in_ranking',
            'total_opponents', 'percentile', 'created_at', 'updated_at',
            'completed_at', 'error_message', 'is_paid', 'opponent_ratings'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'user_current_rating', 
            'user_position_in_ranking', 'total_opponents', 'percentile',
            'created_at', 'updated_at', 'completed_at', 'error_message'
        ]

class CreateAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessAnalysis
        fields = ['chess_username', 'end_date', 'game_mode']
        
    def validate_chess_username(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Chess username must be at least 3 characters long.")
        return value.strip()

class AnalysisCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisCache
        fields = ['username', 'game_mode', 'rating', 'cached_at']
