# import requests
# from time import sleep
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# #from entities.User import User
#
# url = 'https://api.telegram.org/bot520393283:AAHtkSuQ2xx5UUy23evxPaPM3IjieGt9WG4/'
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
if __name__ == '__main__':
    main()