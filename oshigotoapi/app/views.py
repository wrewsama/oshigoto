from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def test(req):
    return Response({"message": "ayo you love shiorin too?"})