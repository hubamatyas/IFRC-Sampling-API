from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('state-list/', views.stateList, name='state-list'),
    path('option-list/', views.optionList, name='option-list'),
    path('decision-tree/<int:state_id>/', views.decisionTree, name='decision-tree'),
    path('simple-random/sample-size/', views.simpleRandom, name='calculate_simple_random')
]
