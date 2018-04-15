from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import constants_list
import telegram_functions
from entity.User import User as User


# def create_reminder(session, user, date, time, text, circle_type=None, circle_parameter=None):
#     reminder = Reminder(user.get_id, text, date, time, circle_type, circle_parameter)
#     session.add(reminder)
#     session.commit()
#     if reminder.circle_type != CircleType.none_circle:
#         create_child_reminder(session, reminder, True)
#     return 1
#
#
# def create_child_reminder(session, parent_reminder, is_first_time, old_date=None):
#     if is_first_time:
#         new_date = parent_reminder.date
#     else:
#         if parent_reminder.circle_type == CircleType.none_circle:
#             return
#         elif parent_reminder.circle_type == CircleType.year_circle:
#             new_date = datetime.date()
#         elif parent_reminder.circle_type == CircleType.month_circle:
#             pass
#         elif parent_reminder.circle_type == CircleType.week_circle:
#             pass
#         elif parent_reminder.circle_type == CircleType.day_circle:
#             pass
#
#     child_reminder = Reminder(parent_reminder.user_id, parent_reminder.text, new_date,
#                               parent_reminder.time, parent_reminder_id=parent_reminder.id)
#     session.add(child_reminder)
#     session.commit()
#
#
# def edit_reminder_handler(isCircle, user):
#     if isCircle:
#         reminder_list = session.query(Reminder).filter(Reminder.user_id == user.get_id,
#                                                        Reminder.circle_type != CircleType.none_circle,
#                                                        Reminder.is_complete == False).order_by(Reminder.date).all()
#     else:
#         reminder_list = session.query(Reminder).filter(Reminder.user_id == user.get_id,
#                                                        Reminder.circle_type == CircleType.none_circle,
#                                                        Reminder.is_complete == False,
#                                                        Reminder.date <= (
#                                                            datetime.datetime.now().date() + datetime.timedelta(
#                                                                VISIBLE_PERIOD))
#                                                        ).order_by(Reminder.date).all()
#     print('*' * 100)
#     for reminder in reminder_list:
#         print(str(reminder_list.index(reminder) + 1) + ') ' + str(reminder))
#     print('*' * 100)
#     inp = input('Выберите необходимое напоминание(или "e" для возврата): ')
#     if inp == 'e' or int(inp) < 0 or int(inp) > len(reminder_list):
#         return False
#     else:
#         rem_selected = int(inp) - 1
#     print('**** ' + str(reminder_list[rem_selected]))
#     print('''Выберите действие с напоминанием:
#                         1 - завершить напоминание
#                         2 - редактировать напоминание
#                         3 - удалить напоминание
#                         4 - вернуться назад
#                     ''')
#     rem_action = int(input('Введите действие: '))
#     if rem_action == 1:
#         if reminder_list[rem_selected].circle_type != CircleType.none_circle:
#             circle_rem = session.query(Reminder).filter(Reminder.id ==
#                                                         reminder_list[rem_selected].parent_reminder_id).all()[0]
#             new_child_date = reminder_list[rem_selected].calculate_next_child_reminder_date(
#                 reminder_list[rem_selected].date,
#                 circle_rem.circle_type)
#             new_reminder = Reminder(reminder_list[rem_selected].user_id, reminder_list[rem_selected].text,
#                                     new_child_date, reminder_list[rem_selected].time,
#                                     parent_reminder_id=reminder_list[rem_selected].parent_reminder_id)
#             session.add(new_reminder)
#             session.commit()
#         # *****
#         reminder_list[rem_selected].setComplete(True)
#         session.commit()
#     elif rem_action == 2:
#         print('''Что необходимо отредактировать:
#                                         1 - тескт
#                                         2 - дату
#                                         3 - время
#                                         4 - вернуться назад
#                                     ''')
#         edit_part = int(input('Что редактировать? :'))
#         if edit_part == 1:
#             new_text = input('Введите новый текст: ')
#             reminder_list[rem_selected].setText(new_text)
#             session.commit()
#         elif edit_part == 2:
#             new_date = extract_date(input('Введите новую дату: '))
#             reminder_list[rem_selected].setDate(new_date)
#             session.commit()
#         elif edit_part == 3:
#             new_time = extract_time(input('Введите новое время: '))
#             reminder_list[rem_selected].setTime(new_time)
#             session.commit()
#         elif edit_part == 4:
#             return False
#     elif rem_action == 3:
#         circle_rem = session.query(Reminder).filter(Reminder.id ==
#                                                     reminder_list[rem_selected].parent_reminder_id).all()[0]
#         new_child_date = reminder_list[rem_selected].calculate_next_child_reminder_date(
#             reminder_list[rem_selected].date,
#             circle_rem.circle_type)
#         new_reminder = Reminder(reminder_list[rem_selected].user_id, reminder_list[rem_selected].text,
#                                 new_child_date, reminder_list[rem_selected].time,
#                                 parent_reminder_id=reminder_list[rem_selected].parent_reminder_id)
#         session.add(new_reminder)
#         session.commit()
#         # **********
#         session.delete(reminder_list[rem_selected])
#         session.commit()
#     elif rem_action == 4:
#         return False
#     else:
#         return False
#     return True
#
#
def user_entry(session, message):
    first_name = ''
    last_name = ''
    if 'callback_query' in message.keys():
        telegram_user_id = int(message['callback_query']['from']['id'])
    else:
        telegram_user_id = int(message['message']['from']['id'])

    user_search = session.query(User).filter(User.telegram_user_id == telegram_user_id).all()
    if len(user_search) == 0:
        try:
            first_name = message['message']['from']['first_name']
        except:
            pass
        try:
            last_name = message['message']['from']['last_name']
        except:
            pass

        user = User(first_name, last_name, telegram_user_id)
        telegram_functions.send_message(chat=message['message']['chat']['id'], text='Вы - новый пользователь')
        return user
    else:
        return user_search[0]


# Telegram Handler functions *******************************************************************************************

if __name__ == '__main__':
    print(constants_list.API_TELEGRAM_URL)
    engine = create_engine(constants_list.COONECTION_STRING, client_encoding='utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    # ****
    while True:
        try:
            updates = telegram_functions.get_updates_json()
        except:
            continue
        for message in updates['result']:
            user = user_entry(session, message)
            user.process_message(session, message)
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
