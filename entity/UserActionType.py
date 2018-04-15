import enum

class UserActionType(enum.Enum):
    main_menu = 'main_menu'
    reminder_ready = 'reminder_ready'
    date_request = 'date_request'
    date_input = 'date_input'
    time_request = 'time_request'
    time_input = 'time_input'
    text_request = 'text_request'
    text_input = 'text_input'
    is_circle_reminder_request = 'is_circle_reminder_request'
    is_circle_reminder_input = 'is_circle_reminder_input'
    circle_reminder_type_request = 'circle_reminder_type_request'
    circle_reminder_type_input = 'circle_reminder_type_input'