import os
COONECTION_STRING = "postgresql+pg8000://postgres:123@localhost/remember_me"
# ***
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
TELEGRAM_TOKEN = open(os.getcwd() + r'\tokens\telegram_token.txt', 'r').read()
API_TELEGRAM_URL = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/'