from rest_framework.response import Response
from adrf.decorators import api_view
from app.scraperservice import ScraperService

svc = ScraperService()

@api_view(['POST'])
def setLocation(req):
    print("setting location to: " + req.data["location"])
    svc.setLocation(req.data["location"])
    return Response({"message": "ayo you love shiorin too?"})

@api_view(['POST'])
async def search(req):
    print("searching for: " + req.data["query"])
    await svc.search(req.data["query"])
    return Response({"message": "ayo you love shiorin too?"})