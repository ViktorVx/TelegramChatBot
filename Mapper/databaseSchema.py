from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reminders = relationship("Reminder", backref="user")

    @property
    def get_id(self):
        return self.id

    def __init__(self, user_id, first_name, last_name):
        self.id = int(user_id)
        self.first_name = str(first_name)
        self.last_name = str(last_name)

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

    def __init__(self, user_id, text, date, time, circle_type=None, circle_parameter=None, \
                 parent_reminder_id=None):
        self.user_id = user_id
        self.text = text
        self.date = date
        self.time = time
        self.circle_type = circle_type
        self.circle_parameter = circle_parameter
        self.is_complete = False
        self.parent_reminder_id = parent_reminder_id


db_name = 'remember_me'
engine = create_engine("postgresql+pg8000://postgres:123@localhost/" + db_name, \
                       client_encoding='utf8')
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
