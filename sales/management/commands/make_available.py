from django.core.management.base import BaseCommand, CommandError
from sales.models import CarInfo

class Command(BaseCommand):
    help = 'Set the car with given ID as available'

    def add_arguments(self, parser):
        parser.add_argument('car_info_ids', nargs='+', type=int)
        parser.add_argument('--opt_cars', nargs='+', type=int)

    def handle(self, *args, **options):
        # breakpoint()
        for car_info_id in options['car_info_ids']:
            try:
                car_info = CarInfo.objects.get(pk=car_info_id)
            except CarInfo.DoesNotExist:
                # raise CommandError('Poll "%s" does not exist' % car_info_id)
                self.stdout.write(self.style.ERROR(f'Car with ID: {car_info_id} does not exist.'))
                continue
            car_info.status = "available"
            car_info.save()

            self.stdout.write(self.style.SUCCESS('Successfully updated cars "%s"' % car_info_id))
"D:/Webllisto/Django Webllisto/webl/Scripts/activate"