import telegram_functions
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import constants_list
import common_utils
from entity.UserActionType import UserActionType as UserActionType
from entity.CircleType import CircleType as CircleType
from entity.Reminder import Reminder as Reminder
import Mapper



class User(Mapper.Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    reminders = relationship("entity.Reminder.Reminder", backref="user")
    telegram_user_id = Column(Integer, unique=True)
    update_id = Column(Integer)
    user_action = Column(Enum(UserActionType))

    @property
    def get_id(self):
        return self.id

    @property
    def get_update_id(self):
        return int(self.update_id) if self.update_id != None else 0

    @property
    def get_user_action(self):
        return self.user_action

    @property
    def get_current_reminder_circle(self):
        return self.current_reminder_circe

    @property
    def get_current_reminder_date(self):
        return self.current_reminder_date

    def set_current_reminder_date(self, current_reminder_date):
        self.current_reminder_date = current_reminder_date

    @property
    def get_current_reminder_time(self):
        return self.current_reminder_time

    @property
    def get_current_reminder_text(self):
        return self.current_reminder_text

    @property
    def get_current_reminder_circle_type(self):
        return self.current_reminder_circle_type

    @property
    def get_id(self):
        return self.id

    def set_current_reminder_circle_type(self, current_reminder_circle_type):
        self.current_reminder_circle_type = current_reminder_circle_type

    def set_current_reminder_text(self, current_reminder_text):
        self.current_reminder_text = current_reminder_text

    def set_current_reminder_time(self, current_reminder_time):
        self.current_reminder_time = current_reminder_time

    def set_current_reminder_circle(self, current_reminder_circle):
        self.current_reminder_circe = current_reminder_circle

    def set_user_action(self, user_action):
        self.user_action = user_action

    def set_update_id(self, update_id):
        self.update_id = int(update_id)

    def __init__(self, first_name, last_name, telegram_user_id):
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.telegram_user_id = telegram_user_id
        # --------------------------------------------
        self.user_action = UserActionType.MAIN_MENU
        self.current_reminder_date = ''
        self.current_reminder_time = ''
        self.current_reminder_text = ''
        self.current_reminder_circe = False
        self.current_reminder_circe_type = ''

    def __repr__(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # ***
    def process_message(self, session, message):
        if 'callback_query' in message.keys():
            self.callback_quary_handler(session, message)
        else:
            self.message_handler(session, message)

    def callback_quary_handler(self, session, message):
        if self.get_update_id < int(message['callback_query']['message']['message_id']):
            callback_data = message['callback_query']['data']
            if callback_data == constants_list.CREATE_REMINDER:
                self.set_user_action(UserActionType.date_request)
                self.create_reminder_handler(message['callback_query']['message']['chat']['id'])
            elif callback_data == constants_list.VIEW_REMINDERS:
                pass
            elif callback_data == constants_list.VIEW_CIRCLE_REMINDERS:
                pass
            elif callback_data == constants_list.CIRCLE_REMINDER_TYPE:
                self.set_current_reminder_circle(True)
                self.set_user_action(UserActionType.circle_reminder_type_request)
                self.create_reminder_handler(message['callback_query']['message']['chat']['id'])
            elif callback_data == constants_list.NON_CIRCLE_REMINDER_TYPE:
                new_reminder = Reminder(self.get_id, self.get_current_reminder_text,
                                        common_utils.extract_date(self.get_current_reminder_date),
                                        common_utils.extract_time(self.get_current_reminder_time))
                session.add(new_reminder)
                session.commit()
                self.set_user_action(UserActionType.reminder_ready)
                self.create_reminder_handler(message['callback_query']['message']['chat']['id'])
            elif callback_data in [constants_list.DAY_CIRCLE, constants_list.WEEK_CIRCLE,
                                   constants_list.MONTH_CIRCLE, constants_list.YEAR_CIRCLE]:
                self.set_current_reminder_circle_type(callback_data)
                rem_circle = CircleType.none_circle
                if self.get_current_reminder_circle_type == constants_list.DAY_CIRCLE:
                    rem_circle = CircleType.day_circle
                elif self.get_current_reminder_circle_type == constants_list.WEEK_CIRCLE:
                    rem_circle = CircleType.week_circle
                elif self.get_current_reminder_circle_type == constants_list.MONTH_CIRCLE:
                    rem_circle = CircleType.month_circle
                elif self.get_current_reminder_circle_type == constants_list.YEAR_CIRCLE:
                    rem_circle = CircleType.year_circle
                new_reminder = Reminder(self.get_id, self.get_current_reminder_text,
                                        common_utils.extract_date(self.get_current_reminder_date),
                                        common_utils.extract_time(self.get_current_reminder_time),
                                        rem_circle, '')
                session.add(new_reminder)
                session.commit()
                self.set_user_action(UserActionType.reminder_ready)
                self.create_reminder_handler(message['callback_query']['message']['chat']['id'])
            else:
                pass
            self.remember_message_id(session, message['callback_query']['message']['message_id'])

    def create_reminder_handler(self, chat_id):
        if self.get_user_action == UserActionType.date_request:
            telegram_functions.send_message(chat_id, 'Введите дату напоминания:')
            self.set_user_action(UserActionType.date_input)
        elif self.get_user_action == UserActionType.time_request:
            telegram_functions.send_message(chat_id, 'Введите время напоминания:')
            self.set_user_action(UserActionType.time_input)
        elif self.get_user_action == UserActionType.text_request:
            telegram_functions.send_message(chat_id, 'Введите текст напоминания:')
            self.set_user_action(UserActionType.text_input)
        elif self.get_user_action == UserActionType.is_circle_reminder_request:
            telegram_functions.is_reminder_circle_selection(chat_id)
            self.set_user_action(UserActionType.is_circle_reminder_input)
        elif self.get_user_action == UserActionType.circle_reminder_type_request:
            telegram_functions.circle_period_selection(chat_id)
            self.set_user_action(UserActionType.circle_reminder_type_input)
        elif self.get_user_action == UserActionType.reminder_ready:
            telegram_functions.send_message(chat_id, 'Напомиание успешно создано!')
            self.set_user_action(UserActionType.main_menu)
            telegram_functions.print_telegram_menu(chat_id)

    def message_handler(self, session, message):
        if self.get_update_id < int(message['message']['message_id']):
            if self.get_user_action == UserActionType.date_input:
                self.set_current_reminder_date(message['message']['text'])
                self.set_user_action(UserActionType.time_request)
                self.create_reminder_handler(message['message']['chat']['id'])
            elif self.get_user_action == UserActionType.time_input:
                self.set_current_reminder_time(message['message']['text'])
                self.set_user_action(UserActionType.text_request)
                self.create_reminder_handler(message['message']['chat']['id'])
            elif self.get_user_action == UserActionType.text_input:
                self.set_current_reminder_text(message['message']['text'])
                self.set_user_action(UserActionType.is_circle_reminder_request)
                self.create_reminder_handler(message['message']['chat']['id'])
            else:
                telegram_functions.print_telegram_menu(message['message']['chat']['id'])
            self.remember_message_id(session, message['message']['message_id'])

    def remember_message_id(self, session, id):
        self.set_update_id(int(id))
        session.add(self)
        session.commit()






# engine = create_engine(constants_list.COONECTION_STRING, client_encoding='utf8')
# Base.metadata.create_all(engine)
