from django.urls import path
from . import views, simpleRandom

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('state-list/', views.stateList, name='state-list'),
    path('option-list/', views.optionList, name='option-list'),
    path('decision-tree/<int:state_id>/', views.decisionTree, name='decision-tree'),
    path('simple-random/sample-size/<int:margin_of_error>/<int:confidence_level>/<int:non_reponse_rate>/<int:subgroups>'
         '/<int:households>/<int:individuals>/', simpleRandom.as_view(), name='calculate_simple_random')
]
