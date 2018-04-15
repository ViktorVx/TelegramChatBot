import requests
import constants_list
import json


def send_message(chat, text):
    params = {'chat_id': chat, 'text': text, 'parse_mode': 'HTML'}
    response = requests.post(constants_list.API_TELEGRAM_URL + 'sendMessage', data=params)
    return response


def is_reminder_circle_selection(chat_id):
    reply = json.dumps({'inline_keyboard': [[{'text': 'ДА', 'callback_data': constants_list.CIRCLE_REMINDER_TYPE}],
                                            [{'text': 'Нет', 'callback_data': constants_list.NON_CIRCLE_REMINDER_TYPE}],
                                            ]})
    params = {'chat_id': chat_id, 'text': 'Напомиание будет циклическим?', 'reply_markup': reply}
    requests.post(constants_list.API_TELEGRAM_URL + 'sendMessage', data=params)


def circle_period_selection(chat_id):
    reply = json.dumps({'inline_keyboard': [[{'text': 'День', 'callback_data': constants_list.DAY_CIRCLE}],
                                            [{'text': 'Неделя', 'callback_data': constants_list.WEEK_CIRCLE}],
                                            [{'text': 'Месяц', 'callback_data': constants_list.MONTH_CIRCLE}],
                                            [{'text': 'Год', 'callback_data': constants_list.YEAR_CIRCLE}]]})
    params = {'chat_id': chat_id, 'text': 'С какой периодичностью?', 'reply_markup': reply}
    requests.post(constants_list.API_TELEGRAM_URL + 'sendMessage', data=params)


def print_telegram_menu(chat_id):
    reply = json.dumps({'inline_keyboard': [[{'text': 'Создать напоминание', 'callback_data': constants_list.CREATE_REMINDER}],
                                            [{'text': 'Просмотреть напоминания', 'callback_data': constants_list.VIEW_REMINDERS}],
                                            [{'text': 'Просмотреть циклические напоминания',
                                              'callback_data': constants_list.VIEW_CIRCLE_REMINDERS}]]})
    params = {'chat_id': chat_id, 'text': 'Выберите действие:', 'reply_markup': reply}
    requests.post(constants_list.API_TELEGRAM_URL + 'sendMessage', data=params)


def get_updates_json():
    response = requests.get(constants_list.API_TELEGRAM_URL + 'getUpdates')
    return response.json()