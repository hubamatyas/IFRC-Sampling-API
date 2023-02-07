from django.shortcuts import render, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StateSerializer, OptionSerializer
from .models import State, Option

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def stateList(request):
    states = State.objects.all()
    serializer = StateSerializer(states, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def optionList(request):
    options = Option.objects.all()
    serializer = OptionSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def decisionTree(request, state_id):
    try:
        state = State.objects.get(id=state_id)
    except State.DoesNotExist:
        return Response(status=404)
        
    state = State.objects.get(id=state_id)
    options = Option.objects.filter(state=state)
    response = {
        'state': StateSerializer(state).data,
        'options': OptionSerializer(options, many=True).data
    }
    return Response(response)