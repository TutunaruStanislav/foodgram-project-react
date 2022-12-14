import csv

from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = ('Command is writing data from csv to chosen model. '
            'Example running this command: '
            '"python manage.py import_csv --path /static/data/users.csv '
            '--model User --app reviews"'
            )

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str,
                            help='path from BASE_DIR', required=True)
        parser.add_argument('--model', type=str,
                            help='Model name', required=True)
        parser.add_argument('--app', type=str,
                            help='App name', required=True)

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR + options['path']
        _model = apps.get_model(options['app'], options['model'])

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            header = next(reader)
            for row in reader:
                _object_dict = {key: value for key, value in zip(header, row)}
                _model.objects.create(**_object_dict)
