import csv
from django.core.management.base import BaseCommand
import logging

from density.models import (
    Doorway,
    Doorway_DPU_Assignment,
    DPU,
    Space,
    Space_Activity,
)

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Clears database tables and loads with fresh data'

    def truncate_tables(self):
        Doorway.objects.all().delete()
        Doorway_DPU_Assignment.objects.all().delete()
        DPU.objects.all().delete()
        Space.objects.all().delete()
        Space_Activity.objects.all().delete()

    def populate_static_data(self):
        spaceA = Space.objects.create(name='Space A')
        spaceB = Space.objects.create(name='Space B')

        doorwayX = Doorway.objects.create(name='Doorway X')
        doorwayZ = Doorway.objects.create(name='Doorway Z')

        DPU283 = DPU.objects.create(id=283, name='DPU 283')
        DPU423 = DPU.objects.create(id=423, name='DPU 423')

        # create these doorway assignments with a 'created' date that is before any of
        # the test data (would normally be the time that the DPU is assigned to the doorway)
        Doorway_DPU_Assignment.objects.create(
            doorway=doorwayX,
            dpu=DPU283,
            created='2018-01-01T00:00:00Z',
            facing_space=spaceA,
            behind_space=None,
        )
        Doorway_DPU_Assignment.objects.create(
            doorway=doorwayZ,
            dpu=DPU423,
            created='2018-01-01T00:00:00Z',
            facing_space=spaceA,
            behind_space=spaceB,
        )

    def populate_csv_data(self):
        class CSV_Columns(object):
            TIMESTAMP = 0
            DIRECTION = 1
            DPU_ID = 2

        class TrafficDirection(object):
            TOWARD = '-1'
            AWAY = '1'

        # create a in-memory lookup for DPUs -> Doorways, so we don't re-query for each csv row
        # Naively assumes DPU/door assignments don't change (since no changes are mentioned in the
        # homework description). The production handling of inserting new DPU data records would
        # need to look up the DPU/Doorway assignment, at the time the data was generated, to determine
        # which spaces to assign the traffic to.
        assignments = Doorway_DPU_Assignment.objects.all()
        dpu_doorways = {a.dpu_id: a for a in assignments}
        LOGGER.debug(dpu_doorways)

        with open('./dpu_data.csv', 'r') as ifs:
            reader = csv.reader(ifs)
            # skip the header row
            next(reader, None)

            for row in reader:
                LOGGER.debug(f'Processing: {row}')
                dpu_id = int(row[CSV_Columns.DPU_ID])
                try:
                    d = dpu_doorways[dpu_id]
                except KeyError:
                    LOGGER.warn(f'Could not find DPU-Space assignment for DPU {dpu_id}')
                    continue

                traffic_direction = row[CSV_Columns.DIRECTION]
                if traffic_direction == TrafficDirection.TOWARD:
                    # traffic coming toward the sensor means someone is leaving the room that the
                    # sensor is facing, so we subtract one from the space that the sensor is facing
                    # and we add one to the room behind the sensor
                    add_space = d.behind_space
                    sub_space = d.facing_space
                elif traffic_direction == TrafficDirection.AWAY:
                    # traffic going away from the sensor means someone is entering the room that the
                    # sensor is facing, so we add one from the space that the sensor is facing
                    # and we subtract one from the room behind the sensor
                    add_space = d.facing_space
                    sub_space = d.behind_space
                else:
                    # we don't know whats going where, best to just move report it and move on
                    LOGGER.warn(f'Invalid traffic direction value detected: {traffic_direction}')
                    continue

                # some doorways might not have Spaces assigned to both sides, only add activity for
                # Spaces we track
                activity_ts = row[CSV_Columns.TIMESTAMP]
                if add_space:
                    Space_Activity.objects.create(
                        activity_ts=activity_ts,
                        space=add_space,
                        count=1
                    )
                if sub_space:
                    Space_Activity.objects.create(
                        activity_ts=activity_ts,
                        space=sub_space,
                        count=-1
                    )

    def handle(self, *args, **kwargs):
        self.truncate_tables()
        self.populate_static_data()
        self.populate_csv_data()

