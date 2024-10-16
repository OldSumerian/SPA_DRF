from django.core.management import BaseCommand

from spa.models import Place, Action


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        def fill(fill_class, data):
            data_for_create = []
            for d in data:
                data_for_create.append(fill_class(**d))
            fill_class.objects.bulk_create(data_for_create)

        # Добавим места
        places = [
            {"pk": 1, "name": "Дом"},
            {"pk": 2, "name": "Работа"},
            {"pk": 3, "name": "Улица"},
        ]
        fill(Place, places)

        # Добавим действия
        actions = [
            {"pk": 1, "name": "Отжимание"},
            {"pk": 2, "name": "Бег"},
            {"pk": 3, "name": "Съесть бургер"},
        ]
        fill(Action, actions)
