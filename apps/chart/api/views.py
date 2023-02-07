from apps.chart.constants import MAX_DELTA_DAYS
from currency_exchange_rates.settings import mongo_client


from rest_framework.views import APIView
from rest_framework.response import Response
from bson.json_util import dumps
from json import loads
from datetime import datetime, timedelta


class RatesListByDate(APIView):
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        date_delta = end_datetime - start_datetime
        date_delta = date_delta.days + 1
        weekend_days = [6, 7]
        business_days_delta = date_delta
        for i in range(date_delta):
            date_item = start_datetime + timedelta(days=i)
            if date_item.isoweekday() in weekend_days:
                business_days_delta -= 1

        if business_days_delta > MAX_DELTA_DAYS:
            return Response({})

        db = mongo_client["exchange_rates"]
        collection = db["rates"]
        rates = collection.find(
            {"date": {"$gte": start_date, "$lte": end_date}}
        )
        rates = loads(dumps(rates))
        for r in rates:
            del r["_id"]
        return Response(rates)

