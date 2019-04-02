from classes.factory import *
from rooms.factory import *
from schedule.factory import *
from users.factory import *


def make_sample_models():
    SemesterFactory.create_batch(size=2)
    CourseFactory.create_batch(size=40)
    ClassFactory.create_batch(size=40)
    UserFactory.create_batch(size=30)
    RoomFactory.create_batch(size=50)
    ItemFactory.create_batch(size=100)
    ScheduleFactory.create_batch(size=1)
