from django.core.management.base import BaseCommand
from ...models import User
from ...models import Consumption
from datetime import datetime as dt
import pytz
import csv
import glob


class Command(BaseCommand):
    help = 'import data. set {} or {}'.format('user_data', 'consumption')

    def add_arguments(self, parser):
        parser.add_argument('csv_name', nargs=1,)

    def handle(self, *args, **options):
        if 'user_data' in options['csv_name']:
            print('import user data...')
            with open('../data/user_data.csv') as csvfile:
                instances = []
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data = User(user_id=row['id'], area=row['area'], tariff=row['tariff'], )
                    instances.append(data)
                User.objects.bulk_create(instances)

        elif 'consumption' in options['csv_name']:
            print('import consumption data...')
            import_files = glob.glob('../data/consumption/*.csv')
            for file in import_files:
                print('saving user_id:{}...'.format(file[-8:-4]))
                instances = []
                with open(file) as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        data = Consumption(user=User.objects.get(user_id=file[-8:-4]), usage_time=dt.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('Asia/Tokyo')), kWh=row['consumption'],)
                        instances.append(data)
                Consumption.objects.bulk_create(instances)
