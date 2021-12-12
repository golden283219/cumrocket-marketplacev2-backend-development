import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.http import JsonResponse, HttpRequest, HttpResponse
from datetime import datetime, timedelta

from blockchain.models import LastPrice

import requests
import json

from blockchain.tasks import sync_blockchain

logger = logging.getLogger(__name__)


class CumRocketPriceAPIView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """
        Return the price of CumRocket
        """
        expires_at = datetime.now() - timedelta(minutes=1)
        last_price = LastPrice.objects.filter(last_price__gt=expires_at).first()
        if last_price:
            prices = last_price.data
            print("show from cache")
        else:
            query_params = (
                "ids=cumrocket&vs_currencies=usd&include_market_cap=true&"
                "include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true"
            )
            url = f"https://api.coingecko.com/api/v3/simple/price?{query_params}"
            prices = json.loads(requests.get(url).content)
            LastPrice.objects.create(data=prices)
            print("retrieving new value")
        return JsonResponse(prices)


@api_view(["GET"])
def sync(request: HttpRequest) -> HttpResponse:
    try:
        sync_blockchain.delay()
    except Exception:
        failure_msg = "Failed to sync blockchain"
        logger.exception(failure_msg)
        return Response(json.dumps({"msg": failure_msg}), status=500)
    else:
        return Response(json.dumps({"msg": "success"}), status=200)
