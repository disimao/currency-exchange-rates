from currency_exchange_rates.settings import mongo_client


from rest_framework.views import APIView
from rest_framework.response import Response
from bson.json_util import dumps
from json import loads


class RatesListByDate(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        db = mongo_client["exchange_rates"]
        collection = db["rates"]
        rates = collection.find(
            {"date": {"$gte": start_date, "$lte": end_date}}
        )
        rates = loads(dumps(rates))
        for r in rates:
            del r["_id"]
        return Response(rates)

