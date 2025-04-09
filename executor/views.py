import json
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from executor.models import Scan
from executor.serializers import ScanSerializer
from executor.tasks import nessusscanner
from django_q.tasks import async_task
import os
from rest_framework.decorators import api_view




# API Function to url /scan
# GET Method returns all Scan Objects
# POST method adds and perform a new scan
@csrf_exempt
def scan_list(request):
    if request.method == 'GET':
        scans = Scan.objects.all().order_by('-scan_id')
        serializer = ScanSerializer(scans, many=True)
        return JsonResponse(serializer.data, safe=False)  
    if request.method == 'POST': 
        data = JSONParser().parse(request)
        if "result_ulr" in data:
            data['result_url'] = json.dumps(data['result_url'])
        serializer = ScanSerializer(data=data)
        if serializer.is_valid():
            o = serializer.save()
            scope = Scan.objects.get(pk=o.scan_id)
            # Initiate scan from here for now
            async_task(nessusscanner,scope)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def scan_detail_page(request):
    try:
        scope = Scan.objects.get(pk=request.GET.get("id"))
    except:
        return JsonResponse({'status': 'false', 'error': 'Scan matching query does not exist.'})
    serializer = ScanSerializer(data=scope.__dict__)
    if serializer.is_valid():
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['DELETE'])
def delete(request):
    try:
        scope = Scan.objects.get(pk=request.GET.get("id"))
        if scope.scan_status != 1:
            scope.delete()
            return JsonResponse({'status': 'true'})
    except:
        return JsonResponse({'status': 'false', 'error':str(sys.exc_info())})
