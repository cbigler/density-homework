from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from density.controllers import space_count
from density.models import Space


@api_view(['GET'])
def get_space_count(request, space_id):
    space = get_object_or_404(Space, pk=space_id)

    ts = request.GET.get('ts', now())
    resp = {
        'space_id': space_id,
        'ts': ts,
        'count': space_count.get_space_count(space, at_ts=ts)
    }
    return Response(resp)

