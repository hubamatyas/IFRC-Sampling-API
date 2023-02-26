from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .SystematicRandom import SystematicRandom
from .serializers import StateSerializer, OptionSerializer
from .models import State, Option
from .SimpleRandom import SimpleRandom


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


@api_view(['POST'])
def simpleRandom(request):
    margin_of_error = float(request.data.get('margin_of_error'))
    # print("margin of error=",margin_of_error)
    confidence_level = int(request.data.get('confidence_level'))
    non_response_rate = float(request.data.get('non_response_rate'))
    subgroups = request.data.get('subgroups')
    households = int(request.data.get('households'))
    individuals = int(request.data.get('individuals'))

    simple_random = SimpleRandom(margin_of_error=margin_of_error, confidence_level=confidence_level,
                                 individuals=individuals, households=households,
                                 non_response_rate=non_response_rate, subgroups=subgroups)
    sample_size = simple_random.get_sample_size()
    print('sample_size=', sample_size)
    response = {
        'sampleSize': sample_size
    }
    # print("sample size sent = ", sample_size)
    return Response(response)


@api_view(['POST'])
def systematicRandom(request):
    margin_of_error = float(request.data.get('margin_of_error'))
    confidence_level = int(request.data.get('confidence_level'))
    non_response_rate = float(request.data.get('non_response_rate'))
    subgroups = int(request.data.get('subgroups'))
    households = int(request.data.get('households'))
    individuals = int(request.data.get('individuals'))
    systematic_random = SystematicRandom(margin_of_error=margin_of_error, confidence_level=confidence_level,
                                         individuals=individuals, households=households,
                                         non_response_rate=non_response_rate, subgroups=subgroups)
    result = systematic_random.get_result()
    response = {
        'Result': result
    }
    # print("result = ",result)
    # print("Sample size sent")
    return Response(response)
