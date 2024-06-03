from django.urls import path
from . import views

urlpatterns = [
    path('machines/', views.MachineList.as_view(), name='machine-list'),
    path('machines/<int:pk>/', views.MachineDetail.as_view(), name='machine-detail'),
    path('production-logs/', views.ProductionLogList.as_view(), name='production-log-list'),
    path('production-logs/<int:pk>/', views.ProductionLogDetail.as_view(), name='production-log-detail'),
    path('oee/', views.OEEList.as_view(),name='oee')
]