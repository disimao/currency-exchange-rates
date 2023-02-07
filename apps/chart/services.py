import requests


from datetime import datetime, timedelta
from urllib import parse


from apps.chart.constants import BASE_URL, RATES_PATH


def get_rates_by_date_from_vatcomply(start_date, end_date, base_rate="USD"):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_date - start_date
    weekend_days = [6, 7]
    rates_url = parse.urljoin(BASE_URL, RATES_PATH)
    rates_list = []
    for i in range(delta.days + 1):
        date_item = start_date + timedelta(days=i)
        if date_item.isoweekday() in weekend_days:
            continue

        response = requests.get(
            rates_url,
            params={
                "date": datetime.strftime(date_item, "%Y-%m-%d"),
                "base": base_rate,
            },
        )

        if response.ok:
            rates = response.json()
            rate_cleaned = {"rates": {}}
            rate_cleaned["date"] = rates.get("date")
            rate_cleaned["base"] = rates.get("base")
            for currency in ["EUR", "USD", "JPY", "BRL"]:
                rate_cleaned["rates"].update(
                    {currency: rates.get("rates").get(currency)}
                )
            rates_list.append(rate_cleaned)
    return rates_list
