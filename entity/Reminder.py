import Mapper
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Enum
from sqlalchemy import ForeignKey
from entity.CircleType import CircleType as CircleType
import datetime



class Reminder(Mapper.Base):
    __tablename__ = 'reminder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('user.id'))
    text = Column(String)
    date = Column(Date)
    time = Column(Time)
    circle_type = Column(Enum(CircleType))
    circle_parameter = Column(String)
    is_complete = Column(Boolean)
    parent_reminder_id = Column(ForeignKey('reminder.id'))

    def __init__(self, user_id, text, date, time, circle_type=CircleType.none_circle, circle_parameter=None, \
                 parent_reminder_id=None):
        self.user_id = user_id
        self.text = text
        self.date = date
        self.time = time
        self.circle_type = circle_type
        self.circle_parameter = circle_parameter
        self.is_complete = False
        self.parent_reminder_id = parent_reminder_id

    def __str__(self):
        return str(self.date) + ' ' + str(self.time) + ' ' + self.text

    def setComplete(self, is_Complete):
        self.is_complete = is_Complete

    def setText(self, text):
        self.text = text

    def setDate(self, date):
        self.date = date

    def setTime(self, time):
        self.time = time

    def calculate_next_child_reminder_date(self, old_date, circle_type):
        if circle_type == CircleType.none_circle:
            return old_date
        elif circle_type == CircleType.day_circle:
            return old_date + + datetime.timedelta(1)
        elif circle_type == CircleType.week_circle:
            return old_date + + datetime.timedelta(7)
        elif circle_type == CircleType.month_circle:
            if old_date.month == 12:
                return old_date.replace(old_date.year + 1, 1)
            else:
                return old_date.replace(old_date.year, old_date.month + 1)
        elif circle_type == CircleType.year_circle:
            return old_date.replace(old_date.year + 1)


# engine = create_engine(constants_list.COONECTION_STRING, client_encoding='utf8')
# Base.metadata.create_all(engine)