import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()
COONECTION_STRING = "postgresql+pg8000://postgres:123@localhost/remember_me"
#COONECTION_STRING = "postgresql+pg8000://SYSDBA:masterkey@localhost/remember_me"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    reminders = relationship("Reminder", backref="user")
    telegram_user_id = Column(Integer, unique=True)

    @property
    def get_id(self):
        return self.id

    def __init__(self, first_name, last_name, telegram_user_id):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.telegram_user_id = telegram_user_id

    def __repr__(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class CircleType(enum.Enum):
    none_circle = 'none_circle'
    day_circle = 'day_circle'
    week_circle = 'week_circle'
    month_circle = 'month_circle'
    year_circle = 'year_circle'


class Reminder(Base):
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
            return old_date.replace(old_date.year+1)


engine = create_engine(COONECTION_STRING, client_encoding='utf8')
Base.metadata.create_all(engine)
