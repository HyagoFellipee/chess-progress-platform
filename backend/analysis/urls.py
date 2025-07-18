from django.urls import path
from . import views

urlpatterns = [
    path('', views.AnalysisListView.as_view(), name='analysis-list'),
    path('create/', views.CreateAnalysisView.as_view(), name='create-analysis'),
    path('<uuid:pk>/', views.AnalysisDetailView.as_view(), name='analysis-detail'),
    path('<uuid:pk>/status/', views.analysis_status, name='analysis-status'),
    path('<uuid:pk>/opponents/', views.opponent_ratings, name='opponent-ratings'),
]
