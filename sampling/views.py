from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .ClusterRandom import ClusterRandom
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
    data = request.data
    margin_of_error = data['margin_of_error']
    confidence_level = data['confidence_level']
    non_response_rate = data['non_response_rate']
    subgroups = data['subgroups']
    households = data['households'] if data['households'] and data['households'] != 0 else None
    individuals = data['individuals'] if data['individuals'] and data['individuals'] != 0 else None

    simple_random = SimpleRandom(margin_of_error=margin_of_error, confidence_level=confidence_level,
                                 individuals=individuals, households=households,
                                 non_response_rate=non_response_rate, subgroups=subgroups)
    try:
        simple_random.start_calculation()
        sample_size = simple_random.get_sample_size()
        response = {
            'status': 'success',
            'sample_size': sample_size
        }
        return Response(response)
    except ValueError as e:
        response = {
            'status': 'error',
            'error_message': str(e)
        }
        return Response(response, status=400)
    except TypeError as e:
        response = {
            'status': 'error',
            'error_message': str(e)
        }
        return Response(response, status=400)


@api_view(['POST'])
def systematicRandom(request):
    data = request.data
    margin_of_error = data['margin_of_error']
    confidence_level = data['confidence_level']
    non_response_rate = data['non_response_rate']
    subgroups = data['subgroups']
    households = data['households'] if data['households'] and data['households'] != 0 else None
    individuals = data['individuals'] if data['individuals'] and data['individuals'] != 0 else None
    systematic_random = SystematicRandom(margin_of_error=margin_of_error, confidence_level=confidence_level,
                                         individuals=individuals, households=households,
                                         non_response_rate=non_response_rate, subgroups=subgroups)
    try:
        systematic_random.start_calculation()
        intervals = systematic_random.get_intervals()
        response = {
            'status': 'success',
            'intervals': intervals
        }
        return Response(response)
    except ValueError as e:
        print(e)
        response = {
            'status': 'error',
            'error_message': str(e)
        }
        return Response(response, status=400)
    except TypeError as e:
        print(e)
        response = {
            'status': 'error',
            'error_message': str(e)
        }
        return Response(response, status=400)


@api_view(['POST'])
def clusterRandom(request):
    data = request.data
    margin_of_error = data['margin_of_error']
    confidence_level = data['confidence_level']
    non_response_rate = data['non_response_rate']
    households = data['households'] if data['households'] and data['households'] != 0 else None
    individuals = data['individuals'] if data['individuals'] and data['individuals'] != 0 else None
    communities = data['locations'] if data['communities'] and data['communities'] != 0 else None
    cluster_random = ClusterRandom(margin_of_error=margin_of_error, confidence_level=confidence_level,
                                   individuals=individuals, households=households,
                                   non_response_rate=non_response_rate, subgroups=None, communities=communities)
    try:
        cluster_random.start_calculation()
        clusters = cluster_random.get_clusters()

        response = {
            'status': 'success',
            'clusters': clusters
        }
        print("clusters = ", clusters)
        return Response(response)
    except ValueError as e:
        print(e)
        response = {
            'status': 'error',
            'error_message': str(e)
        }
        return Response(response, status=400)
    except TypeError as e:
        print(e)
        response = {
            'status': 'error',
            'error_message': str(e)
        }
        return Response(response, status=400)
