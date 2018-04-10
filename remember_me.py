import requests
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Mapper.databaseSchema import User, Reminder, CircleType
import datetime
import os
import json

COONECTION_STRING = "postgresql+pg8000://postgres:123@localhost/remember_me"
# COONECTION_STRING = "postgresql+pg8000://SYSDBA:masterkey@localhost/remember_me"
VISIBLE_PERIOD = 7
# ***
CREATE_REMINDER = 'create_reminder'
VIEW_REMINDERS = 'view_reminders'
VIEW_CIRCLE_REMINDERS = 'view_circle_reminders'

CIRCLE_REMINDER_TYPE = 'circle_reminder_type'
NON_CIRCLE_REMINDER_TYPE = 'non_circle_reminder_type'

DAY_CIRCLE = 'day_circle'
WEEK_CIRCLE = 'week_circle'
MONTH_CIRCLE = 'month_circle'
YEAR_CIRCLE = 'year_circle'
# ***
REMINDER_CREATION_STEP = 0  # 0 - процесс создания напоминания не активирован
                            # 1 - затребование даты напоминания
                            # 2 - введение даты напоминания
                            # 3 - затребование времени напоминания
                            # 4 - введение времени напоминания

REM_DATE = ''
REM_TIME = ''
REM_TEXT = ''
REM_CIRCLE = False
REM_CIRCLE_TYPE = ''
# def print_menu():
#     while True:
#         print("Выберите действие:")
#         print('1 - создать напоминание')
#         print('2 - просмотреть напоминания на сегодня')
#         print('3 - выход')
#         print('*' * 20)
#         print('4 - просмотреть циклические напоминания')
#         action = input('Введите номер: ')
#         if action == '1':
#             create_reminder_handler()
#         if action == '2':
#             if not edit_reminder_handler(False):
#                 break
#         if action == '3':
#             exit()
#         if action == '4':
#             if not edit_reminder_handler(True):
#                 break
#     print_menu()


def create_reminder(session, user, date, time, text, circle_type=None, circle_parameter=None):
    reminder = Reminder(user.get_id, text, date, time, circle_type, circle_parameter)
    session.add(reminder)
    session.commit()
    if reminder.circle_type != CircleType.none_circle:
        create_child_reminder(session, reminder, True)
    return 1


def create_child_reminder(session, parent_reminder, is_first_time, old_date=None):
    if is_first_time:
        new_date = parent_reminder.date
    else:
        if parent_reminder.circle_type == CircleType.none_circle:
            return
        elif parent_reminder.circle_type == CircleType.year_circle:
            new_date = datetime.date()
        elif parent_reminder.circle_type == CircleType.month_circle:
            pass
        elif parent_reminder.circle_type == CircleType.week_circle:
            pass
        elif parent_reminder.circle_type == CircleType.day_circle:
            pass

    child_reminder = Reminder(parent_reminder.user_id, parent_reminder.text, new_date,
                              parent_reminder.time, parent_reminder_id=parent_reminder.id)
    session.add(child_reminder)
    session.commit()


def extract_date(tx_date):
    return datetime.date(int(tx_date[4:]) + 2000, int(tx_date[2:4]), int(tx_date[:2]))


def extract_time(tx_time):
    return datetime.time(int(tx_time[:2]), int(tx_time[2:]))


# def create_reminder_handler(user):
#     tx_date = input('Введите дату напоминания: ')
#     date = extract_date(tx_date)
#     # **********************************************
#     tx_time = input('Введите время напоминания: ')
#     time = extract_time(tx_time)
#     # **********************************************
#     text = input('Введите текст напоминания: ')
#     # **********************************************
#     print('''Напоминание циклическое?
#                 1 - Да
#                 2 - Нет''')
#     tx_is_circle = input()
#     if tx_is_circle == '1':
#         print('''С какой цикличностью?
#                     1 - День
#                     2 - Неделя
#                     3 - Месяц
#                     4 - Год''')
#         tx_circle_type = input()
#         if tx_circle_type == '1':
#             circle_type = CircleType.day_circle
#             circle_parameter = str(extract_time(tx_time))
#         elif tx_circle_type == '2':
#             print('''Введите день недели повтора:
#                         1 - Каждый понедельник
#                         2 - Каждый вторник
#                         3 - Каждую среду
#                         4 - Каждый четверг
#                         5 - Каждую пятницу
#                         6 - Каждую субботу
#                         7 - Каждое воскресенье''')
#             circle_week_day = input()
#             circle_type = CircleType.week_circle
#             circle_parameter = str(circle_week_day)
#         elif tx_circle_type == '3':
#             circle_month_day = input('Введите число месяца повтора: ')
#             circle_type = CircleType.month_circle
#             circle_parameter = str(circle_month_day)
#         elif tx_circle_type == '4':
#             circle_year_day = input('Введите число и месяц повтора: ')
#             circle_type = CircleType.year_circle
#             circle_parameter = str(circle_year_day)
#
#     else:
#         circle_type = CircleType.none_circle
#         circle_parameter = ''
#     # **********************************************
#     if create_reminder(session, user, date, time, text, circle_type, circle_parameter) == 1:
#         print('Напоминание успешно создано!')


def edit_reminder_handler(isCircle, user):
    if isCircle:
        reminder_list = session.query(Reminder).filter(Reminder.user_id == user.get_id,
                                                       Reminder.circle_type != CircleType.none_circle,
                                                       Reminder.is_complete == False).order_by(Reminder.date).all()
    else:
        reminder_list = session.query(Reminder).filter(Reminder.user_id == user.get_id,
                                                       Reminder.circle_type == CircleType.none_circle,
                                                       Reminder.is_complete == False,
                                                       Reminder.date <= (
                                                           datetime.datetime.now().date() + datetime.timedelta(
                                                               VISIBLE_PERIOD))
                                                       ).order_by(Reminder.date).all()
    print('*' * 100)
    for reminder in reminder_list:
        print(str(reminder_list.index(reminder) + 1) + ') ' + str(reminder))
    print('*' * 100)
    inp = input('Выберите необходимое напоминание(или "e" для возврата): ')
    if inp == 'e' or int(inp) < 0 or int(inp) > len(reminder_list):
        return False
    else:
        rem_selected = int(inp) - 1
    print('**** ' + str(reminder_list[rem_selected]))
    print('''Выберите действие с напоминанием:
                        1 - завершить напоминание
                        2 - редактировать напоминание
                        3 - удалить напоминание
                        4 - вернуться назад
                    ''')
    rem_action = int(input('Введите действие: '))
    if rem_action == 1:
        if reminder_list[rem_selected].circle_type != CircleType.none_circle:
            circle_rem = session.query(Reminder).filter(Reminder.id ==
                                                        reminder_list[rem_selected].parent_reminder_id).all()[0]
            new_child_date = reminder_list[rem_selected].calculate_next_child_reminder_date(
                reminder_list[rem_selected].date,
                circle_rem.circle_type)
            new_reminder = Reminder(reminder_list[rem_selected].user_id, reminder_list[rem_selected].text,
                                    new_child_date, reminder_list[rem_selected].time,
                                    parent_reminder_id=reminder_list[rem_selected].parent_reminder_id)
            session.add(new_reminder)
            session.commit()
        # *****
        reminder_list[rem_selected].setComplete(True)
        session.commit()
    elif rem_action == 2:
        print('''Что необходимо отредактировать:
                                        1 - тескт
                                        2 - дату
                                        3 - время
                                        4 - вернуться назад
                                    ''')
        edit_part = int(input('Что редактировать? :'))
        if edit_part == 1:
            new_text = input('Введите новый текст: ')
            reminder_list[rem_selected].setText(new_text)
            session.commit()
        elif edit_part == 2:
            new_date = extract_date(input('Введите новую дату: '))
            reminder_list[rem_selected].setDate(new_date)
            session.commit()
        elif edit_part == 3:
            new_time = extract_time(input('Введите новое время: '))
            reminder_list[rem_selected].setTime(new_time)
            session.commit()
        elif edit_part == 4:
            return False
    elif rem_action == 3:
        circle_rem = session.query(Reminder).filter(Reminder.id ==
                                                    reminder_list[rem_selected].parent_reminder_id).all()[0]
        new_child_date = reminder_list[rem_selected].calculate_next_child_reminder_date(
            reminder_list[rem_selected].date,
            circle_rem.circle_type)
        new_reminder = Reminder(reminder_list[rem_selected].user_id, reminder_list[rem_selected].text,
                                new_child_date, reminder_list[rem_selected].time,
                                parent_reminder_id=reminder_list[rem_selected].parent_reminder_id)
        session.add(new_reminder)
        session.commit()
        # **********
        session.delete(reminder_list[rem_selected])
        session.commit()
    elif rem_action == 4:
        return False
    else:
        return False
    return True


# API functions ********************************************************************************************************

def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()


def get_me_json(request):
    response = requests.get(request + 'getMe')
    return response.json()


def get_last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    if total_updates == -1:
        return ''
    else:
        return results[total_updates]


def get_state():
    response = requests.post(API_TELEGRAM_URL + 'getState')
    return response


# **********************************************************************************************************************
def send_message(chat, text):
    params = {'chat_id': chat, 'text': text, 'parse_mode': 'HTML'}
    response = requests.post(API_TELEGRAM_URL + 'sendMessage', data=params)
    return response


# def send_inline_keyboard(chat_id, text):
#     reply = json.dumps({'inline_keyboard': [[{'text': 'Строка1', 'callback_data': 'str1'}], [{'text': 'Строка2', 'callback_data': 'str2'}]]})
#     params = {'chat_id': chat_id, 'text': 'Перейти на страничку автора', 'reply_markup': reply}
#     response = requests.post(API_TELEGRAM_URL + 'sendMessage', data=params)
#     return response


# API functions ********************************************************************************************************
# Telegram Handler functions *******************************************************************************************
def callback_quary_handler(session, message):
    global REMINDER_CREATION_STEP
    global REM_CIRCLE, REM_CIRCLE_TYPE
    user = user_entry(session, message)
    if user.get_update_id < int(message['callback_query']['message']['message_id']):
        callback_data = message['callback_query']['data']
        if callback_data==CREATE_REMINDER:
            create_reminder_handler(message['callback_query']['message']['chat']['id'])
        elif callback_data==VIEW_REMINDERS:
            pass
        elif callback_data==VIEW_CIRCLE_REMINDERS:
            pass
        elif callback_data==CIRCLE_REMINDER_TYPE:
            REM_CIRCLE = True
            REMINDER_CREATION_STEP = 8
            create_reminder_handler(message['callback_query']['message']['chat']['id'])
        elif callback_data==NON_CIRCLE_REMINDER_TYPE:
            REM_CIRCLE = False
            REMINDER_CREATION_STEP = 8
            create_reminder_handler(message['callback_query']['message']['chat']['id'])
        elif callback_data in [DAY_CIRCLE, WEEK_CIRCLE, MONTH_CIRCLE, YEAR_CIRCLE]:
            REM_CIRCLE_TYPE = callback_data
            REMINDER_CREATION_STEP = 9
            create_reminder_handler(message['callback_query']['message']['chat']['id'])
        else:
            pass
        remember_message_id(session, user, message['callback_query']['message']['message_id'])


def message_handler(session, message):
    global REMINDER_CREATION_STEP
    global REM_DATE, REM_TIME, REM_TEXT
    user = user_entry(session, message)
    if user.get_update_id < int(message['message']['message_id']):
        if REMINDER_CREATION_STEP==1:
            REM_DATE = message['message']['text']
            REMINDER_CREATION_STEP = 2
            create_reminder_handler(message['message']['chat']['id'])
        elif REMINDER_CREATION_STEP==3:
            REM_TIME = message['message']['text']
            REMINDER_CREATION_STEP = 4
            create_reminder_handler(message['message']['chat']['id'])
        elif REMINDER_CREATION_STEP==5:
            REM_TEXT = message['message']['text']
            REMINDER_CREATION_STEP = 6
            create_reminder_handler(message['message']['chat']['id'])
        else:
            print_telegram_menu(message['message']['chat']['id'])
        remember_message_id(session, user, message['message']['message_id'])



def create_reminder_handler(chat_id):
    global REMINDER_CREATION_STEP
    if REMINDER_CREATION_STEP == 0:
        send_message(chat_id, 'Введите дату напоминания:')
        REMINDER_CREATION_STEP = 1
    elif REMINDER_CREATION_STEP == 2:
        send_message(chat_id, 'Введите время напоминания:')
        REMINDER_CREATION_STEP = 3
    elif REMINDER_CREATION_STEP ==4:
        send_message(chat_id, 'Введите текст напоминания:')
        REMINDER_CREATION_STEP = 5
    elif REMINDER_CREATION_STEP == 6:
        is_reminder_circle_selection(chat_id)
        REMINDER_CREATION_STEP = 7
    elif REMINDER_CREATION_STEP ==8:
        pass
    # tx_date = input('Введите дату напоминания: ')
    # date = extract_date(tx_date)
    # # **********************************************
    # tx_time = input('Введите время напоминания: ')
    # time = extract_time(tx_time)
    # # **********************************************
    # text = input('Введите текст напоминания: ')
    # # **********************************************
    # print('''Напоминание циклическое?
    #             1 - Да
    #             2 - Нет''')
    # tx_is_circle = input()
    # if tx_is_circle == '1':
    #     print('''С какой цикличностью?
    #                 1 - День
    #                 2 - Неделя
    #                 3 - Месяц
    #                 4 - Год''')
    #     tx_circle_type = input()
    #     if tx_circle_type == '1':
    #         circle_type = CircleType.day_circle
    #         circle_parameter = str(extract_time(tx_time))
    #     elif tx_circle_type == '2':
    #         print('''Введите день недели повтора:
    #                     1 - Каждый понедельник
    #                     2 - Каждый вторник
    #                     3 - Каждую среду
    #                     4 - Каждый четверг
    #                     5 - Каждую пятницу
    #                     6 - Каждую субботу
    #                     7 - Каждое воскресенье''')
    #         circle_week_day = input()
    #         circle_type = CircleType.week_circle
    #         circle_parameter = str(circle_week_day)
    #     elif tx_circle_type == '3':
    #         circle_month_day = input('Введите число месяца повтора: ')
    #         circle_type = CircleType.month_circle
    #         circle_parameter = str(circle_month_day)
    #     elif tx_circle_type == '4':
    #         circle_year_day = input('Введите число и месяц повтора: ')
    #         circle_type = CircleType.year_circle
    #         circle_parameter = str(circle_year_day)
    #
    # else:
    #     circle_type = CircleType.none_circle
    #     circle_parameter = ''
    # # **********************************************
    # if create_reminder(session, user, date, time, text, circle_type, circle_parameter) == 1:
    #     print('Напоминание успешно создано!')


def remember_message_id(session, user, id):
    user.set_update_id(int(id))
    session.add(user)
    session.commit()

# ****************************************
def circle_period_selection(chat_id):
    reply = json.dumps({'inline_keyboard': [[{'text': 'День', 'callback_data': DAY_CIRCLE}],
                                            [{'text': 'Неделя', 'callback_data': WEEK_CIRCLE}],
                                            [{'text': 'Месяц', 'callback_data': MONTH_CIRCLE}],
                                            [{'text': 'Год', 'callback_data': YEAR_CIRCLE}]]})
    params = {'chat_id': chat_id, 'text': 'С какой периодичностью?', 'reply_markup': reply}
    requests.post(API_TELEGRAM_URL + 'sendMessage', data=params)

def print_telegram_menu(chat_id):
    reply = json.dumps({'inline_keyboard': [[{'text': 'Создать напоминание', 'callback_data': CREATE_REMINDER}],
                                            [{'text': 'Просмотреть напоминания', 'callback_data': VIEW_REMINDERS}],
                                            [{'text': 'Просмотреть циклические напоминания',
                                              'callback_data': VIEW_CIRCLE_REMINDERS}]]})
    params = {'chat_id': chat_id, 'text': 'Выберите действие:', 'reply_markup': reply}
    requests.post(API_TELEGRAM_URL + 'sendMessage', data=params)

def is_reminder_circle_selection(chat_id):
    reply = json.dumps({'inline_keyboard': [[{'text': 'ДА', 'callback_data': CIRCLE_REMINDER_TYPE}],
                                            [{'text': 'Нет', 'callback_data': NON_CIRCLE_REMINDER_TYPE}],
                                            ]})
    params = {'chat_id': chat_id, 'text': 'Напомиание будет циклическим?', 'reply_markup': reply}
    requests.post(API_TELEGRAM_URL + 'sendMessage', data=params)

# ****************************************
def user_entry(session, message):
    if 'callback_query' in message.keys():
        telegram_user_id = int(message['callback_query']['from']['id'])
    else:
        telegram_user_id = int(message['message']['from']['id'])

    user_search = session.query(User).filter(User.telegram_user_id == telegram_user_id).all()
    if len(user_search) == 0:
        user = User(message['message']['from']['first_name'], message['message']['from']['last_name'],
                    telegram_user_id)
        send_message(chat=message['message']['chat']['id'], text='Вы - новый пользователь')
        return user
    else:
        return user_search[0]


# Telegram Handler functions *******************************************************************************************

if __name__ == '__main__':
    TELEGRAM_TOKEN = open(os.getcwd() + r'\tokens\telegram_token.txt', 'r').read()
    API_TELEGRAM_URL = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/'
    print(API_TELEGRAM_URL)
    engine = create_engine(COONECTION_STRING, client_encoding='utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    # ****
    # ****
    while True:
        try:
            updates = get_updates_json(API_TELEGRAM_URL)
        except:
            continue
        for message in updates['result']:
            # todo здесь вставить обработку команд
            if 'callback_query' in message.keys():
                callback_quary_handler(session, message)
            else:
                message_handler(session, message)





                # ----------------------------------------------------------------------------------------------------------
                # updates = get_updates_json(API_TELEGRAM_URL)
                # data = get_last_update(updates)
                # if mess_id != data['message']['message_id']:
                #     # text = str(data['message']['from']['id']) + ' ' + data['message']['from']['first_name'] + ' ' + \
                #     #       data['message']['from']['last_name'] + ' : ' + data['message']['text']
                #     # print(text)
                #     # mess_id = data['message']['message_id']
                #     # send_mess(chat=data['message']['chat']['id'], text=text)
                #     telegram_user_id = int(data['message']['from']['id'])
                #     if len(session.query(User).filter(User.telegram_user_id == telegram_user_id).all()) == 0:
                #         user = User(data['message']['from']['first_name'], data['message']['from']['last_name'],
                #                     telegram_user_id)
                #         session.add(user)
                #         session.commit()
                #     else:
                #         user = session.query(User).filter(User.telegram_user_id == telegram_user_id).all()[0]
                #         print(user)
                # sleep(3)
                # ch += 1

                # 127155577
                # ------------------------------------------------------------------------------------------------------------------
                # print("Начинается работа чат-бота")
                # print('*' * 100)
                # # -------------------------------------------------------------------------------------------------------------------
                # user_id = ''
                # while user_id == '':
                #     try:
                #         user_id = int(input('Веедите Ваш id: '))
                #     except:
                #         user_id = ''
                #
                # if len(session.query(User).filter(User.id == user_id).all()) == 0:
                #     first_name = input('Введите first_name: ')
                #     last_name = input('Введите last_name: ')
                #     user = User(user_id, first_name, last_name)
                #     session.add(user)
                #     session.commit()
                # else:
                #     user = session.query(User).filter(User.id == user_id).all()[0]
                #     print('Вы вошли как: ' + str(user))
                # # -------------------------------------------------------------------------------------------------------------------
                # print('*' * 100)
                # # -------------------------------------------------------------------------------------------------------------------
                # print_menu()
