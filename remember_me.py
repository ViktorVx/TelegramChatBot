from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Mapper.databaseSchema import User, Reminder, CircleType
import datetime

COONECTION_STRING = "postgresql+pg8000://postgres:123@localhost/remember_me"
#COONECTION_STRING = "postgresql+pg8000://SYSDBA:masterkey@localhost/remember_me"


def print_menu():
    while True:
        print("Выберите действие:")
        print('1 - создать напоминание')
        print('2 - просмотреть напоминания на сегодня')
        print('3 - выход')
        print('*'*20)
        print('4 - просмотреть циклические напоминания')
        action = input('Введите номер: ')
        if action == '1':
            create_reminder_handler()
        if action == '2':
            reminder_list = session.query(Reminder).filter(Reminder.user_id == user.get_id,
                                                           Reminder.circle_type == CircleType.none_circle,
                                                           Reminder.is_complete == False).order_by(Reminder.date).all()
            print('*' * 100)
            for reminder in reminder_list:
                print(str(reminder_list.index(reminder) + 1) + ') ' + str(reminder))
            print('*' * 100)
            rem_selected = int(input('Выберите необходимое напоминание: ')) - 1
            if rem_selected < 0 or rem_selected > len(reminder_list):
                print('Выход в меню...')
                break
            print('**** ' + str(reminder_list[rem_selected]))
            print('''Выберите действие с напоминанием:
                    1 - завершить напоминание
                    2 - редактировать напоминание
                    3 - удалить напоминание
                    4 - вернуться назад
                ''')
            rem_action = int(input('Введите действие: '))
            if rem_action == 1:
                if reminder_list[rem_selected].circle_type!=CircleType.none_circle:
                    circle_rem = session.query(Reminder).filter(Reminder.id ==
                                                                reminder_list[rem_selected].parent_reminder_id).all()[0]
                    new_child_date = reminder_list[rem_selected].calculate_next_child_reminder_date(reminder_list[rem_selected].date,
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
                    break
            elif rem_action == 3:
                circle_rem = session.query(Reminder).filter(Reminder.id ==
                                                            reminder_list[rem_selected].parent_reminder_id).all()[0]
                new_child_date = reminder_list[rem_selected].calculate_next_child_reminder_date(reminder_list[rem_selected].date,
                                                                                                circle_rem.circle_type)
                new_reminder = Reminder(reminder_list[rem_selected].user_id, reminder_list[rem_selected].text,
                                        new_child_date, reminder_list[rem_selected].time,
                                        parent_reminder_id=reminder_list[rem_selected].parent_reminder_id)
                session.add(new_reminder)
                session.commit()
                #**********
                session.delete(reminder_list[rem_selected])
                session.commit()
            elif rem_action == 4:
                break
            else:
                pass
        if action == '3':
            exit()
        if action == '4':
            circle_reminder_list = session.query(Reminder).filter(Reminder.user_id == user.get_id,
                                                           Reminder.circle_type != CircleType.none_circle,
                                                           Reminder.is_complete == False).order_by(Reminder.date).all()
            print('*' * 100)
            for reminder in circle_reminder_list:
                print(str(circle_reminder_list.index(reminder) + 1) + ') ' + str(reminder))
            print('*' * 100)
            rem_selected = int(input('Выберите необходимое напоминание: ')) - 1
            if rem_selected < 0 or rem_selected > len(circle_reminder_list):
                print('Выход в меню...')
                break
            print('**** ' + str(circle_reminder_list[rem_selected]))
            print('''Выберите действие с напоминанием:
                    1 - завершить напоминание
                    2 - редактировать напоминание
                    3 - удалить напоминание
                    4 - вернуться назад
                ''')
            rem_action = int(input('Введите действие: '))
            if rem_action == 1:
                child_rem_list = session.query(Reminder).filter(Reminder.parent_reminder_id == circle_reminder_list[rem_selected].id).all()
                for child_rem in child_rem_list:
                    child_rem.setComplete(True)
                circle_reminder_list[rem_selected].setComplete(True)
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
                    circle_reminder_list[rem_selected].setText(new_text)
                    session.commit()
                elif edit_part == 2:
                    new_date = extract_date(input('Введите новую дату: '))
                    circle_reminder_list[rem_selected].setDate(new_date)
                    session.commit()
                elif edit_part == 3:
                    new_time = extract_time(input('Введите новое время: '))
                    circle_reminder_list[rem_selected].setTime(new_time)
                    session.commit()
                elif edit_part == 4:
                    break
            elif rem_action == 3:
                child_rem_list = session.query(Reminder).filter(
                    Reminder.parent_reminder_id == circle_reminder_list[rem_selected].id).all()
                for child_rem in child_rem_list:
                    session.delete(child_rem)
                session.commit()
                session.delete(circle_reminder_list[rem_selected])
                session.commit()
            elif rem_action == 4:
                break
            else:
                pass
    print_menu()


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


def create_reminder_handler():
    tx_date = input('Введите дату напоминания: ')
    date = extract_date(tx_date)
    # **********************************************
    tx_time = input('Введите время напоминания: ')
    time = extract_time(tx_time)
    # **********************************************
    text = input('Введите текст напоминания: ')
    # **********************************************
    print('''Напоминание циклическое? 
                1 - Да 
                2 - Нет''')
    tx_is_circle = input()
    if tx_is_circle == '1':
        print('''С какой цикличностью?
                    1 - День
                    2 - Неделя
                    3 - Месяц
                    4 - Год''')
        tx_circle_type = input()
        if tx_circle_type == '1':
            circle_type = CircleType.day_circle
            circle_parameter = str(extract_time(tx_time))
        elif tx_circle_type == '2':
            print('''Введите день недели повтора: 
                        1 - Каждый понедельник
                        2 - Каждый вторник
                        3 - Каждую среду
                        4 - Каждый четверг
                        5 - Каждую пятницу
                        6 - Каждую субботу
                        7 - Каждое воскресенье''')
            circle_week_day = input()
            circle_type = CircleType.week_circle
            circle_parameter = str(circle_week_day)
        elif tx_circle_type == '3':
            circle_month_day = input('Введите число месяца повтора: ')
            circle_type = CircleType.month_circle
            circle_parameter = str(circle_month_day)
        elif tx_circle_type == '4':
            circle_year_day = input('Введите число и месяц повтора: ')
            circle_type = CircleType.year_circle
            circle_parameter = str(circle_year_day)

    else:
        circle_type = CircleType.none_circle
        circle_parameter = ''
    # **********************************************
    if create_reminder(session, user, date, time, text, circle_type, circle_parameter) == 1:
        print('Напоминание успешно создано!')


if __name__ == '__main__':
    engine = create_engine(COONECTION_STRING, client_encoding='utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    # ------------------------------------------------------------------------------------------------------------------
    print("Начинается работа чат-бота")
    print('*' * 100)
    # -------------------------------------------------------------------------------------------------------------------
    user_id = ''
    while user_id == '':
        try:
            user_id = int(input('Веедите Ваш id: '))
        except:
            user_id = ''

    if len(session.query(User).filter(User.id == user_id).all()) == 0:
        first_name = input('Введите first_name: ')
        last_name = input('Введите last_name: ')
        user = User(user_id, first_name, last_name)
        session.add(user)
        session.commit()
    else:
        user = session.query(User).filter(User.id == user_id).all()[0]
        print('Вы вошли как: ' + str(user))
    # -------------------------------------------------------------------------------------------------------------------
    print('*' * 100)
    # -------------------------------------------------------------------------------------------------------------------
    print_menu()






    # if user_id== '':
    #    pass
    #    user_id = 127155577
    #     user = session.query(User).filter(User.user_id == user_id).all()[0]
    # else:
    #     # if len(session.query(User).filter(User.user_id==user_id).all())==0:
    #     first_name = input('Введите first_name:')
    #     last_name = input('Введите last_name:')
    #     #user = User(user_id, first_name, last_name)
    #     user = User(1, "Test", "Testovich")
    #     session.add(user)
    #     session.commit()
    #     # else:
    #     #     user = session.query(User).filter(User.user_id==user_id).all()[0]
    # print('*** ', str(user.user_id), user.first_name, user.last_name)
    # #-------------------------------------------------------------------------------------------------------------------
    # text = ''
    # while text!= 'exit':
    #     text = input('Создать напоминание:')
    #     if text=='+':
    #         rem_text = input('Введите текст напоминания:')
    #         #--------------------------------
    #         rem_date = input('Введите дату:')
    #         date = datetime.date(2018,3,31)
    #         # --------------------------------
    #         rem_time = input('Введите время:')
    #         time = datetime.time(6,0)
    #         # --------------------------------
    #         # reminder = Reminder(user.user_id, rem_text, date, time)
    #         # session.add(reminder)
    #         # session.commit()
    # import requests
    # from time import sleep
    # from sqlalchemy import create_engine
    # from sqlalchemy.orm import sessionmaker
    # #from entities.User import User
    #
    # url = 'https://api.telegram.org/'
    #
    #
    # def get_updates_json(request):
    #     response = requests.get(request + 'getUpdates')
    #     return response.json()
    #
    #
    # def get_me_json(request):
    #     response = requests.get(request + 'getMe')
    #     return response.json()
    #
    #
    # def get_last_update(data):
    #     results = data['result']
    #     total_updates = len(results) - 1
    #     return results[total_updates]
    #
    #
    # def send_mess(chat, text):
    #     params = {'chat_id': chat, 'text': text}
    #     response = requests.post(url + 'sendMessage', data=params)
    #     return response
    #
    # def main():
    #     #print(get_me_json(url))
    #     #print('*' * 100)#---------------------------------------------------------------------------------------------------
    #     # for elem in get_updates_json(url)['result']:
    #     #     print(elem)
    #     #print('*' * 100)#---------------------------------------------------------------------------------------------------
    #     ch = 0
    #     mess_id = 0
    #     # ---------------------------------------------------------------------------------------------------
    #     engine = create_engine("postgresql+pg8000://postgres:123@localhost/remember_me", \
    #                            client_encoding='utf8')
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     # ---------------------------------------------------------------------------------------------------
    #     while ch<100:
    #         data = get_last_update(get_updates_json(url))
    #         if mess_id!= data['message']['message_id']:
    #             text = str(data['message']['from']['id']) + ' ' + data['message']['from']['first_name'] + ' ' + \
    #                   data['message']['from']['last_name'] + ' : ' + data['message']['text']
    #             print(text)
    #             mess_id = data['message']['message_id']
    #             send_mess(chat=data['message']['chat']['id'], text=text)
    #             if len(session.query(User).filter(User.user_id==127155577).all())==0:
    #                 user = User(data['message']['from']['id'], data['message']['from']['first_name'], data['message']['from']['last_name'])
    #                 session.add(user)
    #                 session.commit()
    #
    #         sleep(3)
    #         ch+=1
    #
    #
    # if __name__ == '__main__':
    #    main()
