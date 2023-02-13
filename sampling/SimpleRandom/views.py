from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SimpleRandomSerializer
from .models import SimpleRandom

@api_view(['POST'])
def SimpleRandom(request):
    ps = request.data.get('ps')
    moe = request.data.get('moe')
    ci = request.data.get('ci')
    calculator = SimpleRandom(ps = ps, moe=moe,ci=ci)
    result = calculator.calc()
    response = {
        'sample size': result
    }
    return Response(response)
