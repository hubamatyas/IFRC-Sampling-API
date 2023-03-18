from django.urls import path
from . import views, SimpleRandom, SystematicRandom

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('state-list/', views.stateList, name='state-list'),
    path('option-list/', views.optionList, name='option-list'),
    path('decision-tree/<int:state_id>/', views.decisionTree, name='decision-tree'),
    path('simple-random/', views.simpleRandom, name='simpleRandom'),
    path('systematic-random/', views.systematicRandom, name='systematicRandom'),
    path('time-location/',views.timeLocation,name='timeLocation'),
    path('cluster-random/', views.clusterRandom, name='clusterRandom')
]
