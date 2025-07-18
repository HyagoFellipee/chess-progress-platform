from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import ChessAnalysis, OpponentRating, AnalysisCache
from .serializers import (
    ChessAnalysisSerializer, 
    CreateAnalysisSerializer,
    OpponentRatingSerializer,
    AnalysisCacheSerializer
)

class AnalysisListView(generics.ListAPIView):
    """List all analyses for the authenticated user"""
    serializer_class = ChessAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChessAnalysis.objects.filter(user=self.request.user)

class CreateAnalysisView(generics.CreateAPIView):
    """Create a new chess analysis"""
    serializer_class = CreateAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        analysis = serializer.save(user=self.request.user)
        # TODO: Start Celery task for processing
        # from .tasks import process_chess_analysis
        # task = process_chess_analysis.delay(str(analysis.id))
        # analysis.celery_task_id = task.id
        # analysis.save()
        return analysis
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        analysis = self.perform_create(serializer)
        
        return Response({
            'id': str(analysis.id),
            'message': 'Analysis created successfully!',
            'status': analysis.status,
            'chess_username': analysis.chess_username,
            'game_mode': analysis.game_mode,
            'end_date': analysis.end_date
        }, status=status.HTTP_201_CREATED)

class AnalysisDetailView(generics.RetrieveAPIView):
    """Get details of a specific analysis"""
    serializer_class = ChessAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChessAnalysis.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analysis_status(request, pk):
    """Get the current status of an analysis"""
    analysis = get_object_or_404(ChessAnalysis, id=pk, user=request.user)
    
    return Response({
        'id': str(analysis.id),
        'status': analysis.status,
        'progress': get_analysis_progress(analysis),
        'error_message': analysis.error_message,
        'completed_at': analysis.completed_at,
        'created_at': analysis.created_at,
        'chess_username': analysis.chess_username,
        'game_mode': analysis.game_mode,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def opponent_ratings(request, pk):
    """Get opponent ratings for a specific analysis"""
    analysis = get_object_or_404(ChessAnalysis, id=pk, user=request.user)
    opponents = OpponentRating.objects.filter(analysis=analysis)
    serializer = OpponentRatingSerializer(opponents, many=True)
    
    return Response({
        'analysis_id': str(analysis.id),
        'total_opponents': opponents.count(),
        'user_rating': analysis.user_current_rating,
        'user_position': analysis.user_position_in_ranking,
        'percentile': analysis.percentile,
        'opponents': serializer.data
    })

def get_analysis_progress(analysis):
    """Calculate analysis progress percentage"""
    if analysis.status == 'completed':
        return 100
    elif analysis.status == 'processing':
        # TODO: Get actual progress from Celery task
        return 50
    elif analysis.status == 'failed':
        return 0
    else:  # pending
        return 0
