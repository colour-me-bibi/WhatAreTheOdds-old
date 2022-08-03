from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Scenario
from .serializers import ScenarioSerializer


@api_view(['GET'])
def health(request):
    return Response({'status': 'OK'})


@api_view(['GET', 'POST'])
def scenarios(request):
    if request.method == 'GET':  # returns all scenarios
        scenarios = Scenario.objects.all()
        serializer = ScenarioSerializer(scenarios, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':  # creates a new scenario
        serializer = ScenarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def scenario(request, pk):
    try:
        scenario = Scenario.objects.get(pk=pk)
    except Scenario.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ScenarioSerializer(scenario)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ScenarioSerializer(scenario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        scenario.delete()
        return Response(status=204)
