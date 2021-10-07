#Python
import csv
from os import name
from yubi.boxes.models.box import Box

def load_data_csv(file):
    with open(file, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for i in reader:
            box = Box.objects.create(name=i['name'],
                slug_name=i['slug_name'],
                is_public=i['is_public'],
                is_verified=i['verified'],
                member_limited=i['members_limit']
            )
        box.save()
