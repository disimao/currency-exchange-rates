from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError


from apps.chart.services import get_rates_by_date_from_vatcomply
from utils import get_db_handle


class Command(BaseCommand):
    help = "Stores exchange rates data from every time"

    def handle(self, *args, **options):
        mongo_client = get_db_handle("localhost", 27017, "root", "mongodb")
        db = mongo_client["exchange_rates"]
        collection = db["rates"]
        #A date parameter returns historical rates data for any date since 04.01.1999.
        start_date = datetime.strptime("1999-01-04", "%Y-%m-%d")
        for i in range(8797):
            try:
                str_start_date = datetime.strftime(start_date, "%Y-%m-%d")
                ret_list = get_rates_by_date_from_vatcomply(str_start_date, str_start_date)
                if len(ret_list):
                    collection.insert_one(ret_list[0])
            except:
                raise CommandError(f"Error {start_date}")

            self.stdout.write(
                self.style.SUCCESS(f"Successfully populated date {start_date}")
            )
            start_date = start_date + timedelta(1)
