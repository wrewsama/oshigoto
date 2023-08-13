from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.scraperservice import ScraperService

svc = ScraperService()

@api_view(['POST'])
def setLocation(req):
    print("setting location to: " + req.data["location"])
    svc.setLocation(req.data["location"])
    return Response({"message": "success"})

@api_view(['POST'])
def search(req):
    print("searching for: " + req.data["query"])
    svc.search(req.data["query"])
    return Response({"message": "success"})

@api_view(['GET'])
def getBasicInfo(req):
    print("Getting Basic Info")
    res = svc.getBasicInfo()
    return Response(res)

@api_view(['GET'])
def getTopJobPoints(req):
    print("Getting job points")
    res = svc.getTopJobPoints(int(req.query_params['count']))
    return Response(res)