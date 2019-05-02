import json
import random

from celery.utils.log import get_task_logger
from django.utils import timezone

from atc.celery import app
from classes.models import Class
from rooms.models import Room
from schedule.algorithm import generate
from schedule.models import Schedule, Timeslot, Event
from users.models import User, Group

logger = get_task_logger(__name__)


def get_timespaceslots(tss_data):
    rooms, timeslots, cl, teacher, groups = tss_data
    res = []
    required_capacity = 0
    for i in range(len(groups)):
        required_capacity += User.objects.filter(group=groups[i]).count()
    # TODO: exclude timeslots allocated by professor
    # print("Rooms count={}, Timeslots count={}".format(len(rooms), len(timeslots)))
    for i in range(len(rooms)):
        for j in range(len(timeslots)):
            room = rooms[i]
            slot = timeslots[j]
            priority = 5
            # TODO: may change priority in early morning and late evening
            res.append({
                "slot_id": slot.id * 100000 + room.id,  # f'{{slot.id}_{room.id}}
                "priority": priority
            })
    return res


def prepare_data(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    classes = Class.objects.filter(course__semester=schedule.semester)
    data = []
    timeslots = Timeslot.objects.all()
    rooms = Room.objects.all()

    timespaceslots = []

    for i in range(len(rooms)):
        for j in range(len(timeslots)):
            room = rooms[i]
            slot = timeslots[j]
            timespaceslots.append(slot.id*100000 + room.id)

    for i in range(len(classes)):
        cl = classes[i]
        groups = cl.groups.all()
        class_dict = {
            'teacher_id': cl.teacher.id,
            'course_id': cl.course.id,
            'type_id': cl.type.id,
            'groups_ids': list(map(lambda g: g.id, groups)),
            'timespaceslots': [
                {
                    "slot_id": random.choice(timespaceslots),
                    "priority": 5
                }
            ]
        }
        data.append(class_dict)
    return data, timespaceslots


@app.task
def generate_table():
    logger.info("Preparing data for the generation of the last schedule")
    json_data, timespaceslots = prepare_data(schedule_id=Schedule.objects.last().id)
    if len(json_data) == 0:
        logger.info("No data for generation, aborting")
        return None
    logger.info("Starting generation")
    result = generate(json_data, timespaceslots)
    logger.info("Generation finished")
    return result


@app.task
def generate_table_and_save():
    result = generate_table()
    schedule = Schedule.objects.last()
    for r in result:
        current_class = Class.objects.get(
                course_id=r['course_id'],
                type_id=r['type_id'],
                teacher_id=r['teacher_id']
            )

        event = Event.objects.create(
            current_class=current_class,
            schedule=schedule,
            room_id=r['timespaceslot_id'] % 100000,
            timeslot_id=r['timespaceslot_id'] / 100000,
            date=timezone.now()
        )
        event.save()
        for j in r['groups_ids']:
            event.group.add(j)

    logger.info("Schedule saved")
    return result
