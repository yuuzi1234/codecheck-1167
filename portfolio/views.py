from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, QueryDict
from django.core import serializers
from rest_framework import viewsets
from django.utils.six import BytesIO
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Projects
from .serializers import ProjectsSerializer

# Create your views here.
class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def project_list(request):
    if request.method == "GET":
        project = Projects.objects.all()
        serializer = ProjectsSerializer(project, many=True)
        return JSONResponse(serializer.data)

    elif request.method == "POST":
        query = QueryDict(request.body)
        project = Projects(
            title=query.get('title'),
            description=query.get('description'),
            url=query.get('url'),
        )
        serializer = ProjectsSerializer(project)
        content = JSONRenderer().render(serializer.data)
        data = JSONParser().parse(BytesIO(content))
        serializer = ProjectsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)
    return JSONResponse(status=404)

@csrf_exempt
def project_detail(request, pk):
    try:
        project = Projects.objects.get(pk=pk)
    except Projects.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = ProjectsSerializer(project)
        return JSONResponse(serializer.data)

    elif request.method == "DELETE":
        print(request.body)
        project.delete()
        return JSONResponse([], status=200)
    return HttpResponse(status=500)
