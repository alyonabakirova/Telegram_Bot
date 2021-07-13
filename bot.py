from telebot import *
import requests

bot = telebot.TeleBot('1806208816:AAEZaHOsy95Z3Yf347rTRzcpBO3Tg8g1g0w')

URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
TOKEN = "d6c4e6cc7f93ad1ff6b8e8c76528d501135eb7ec"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Приветствую! Введите ИНН компании. ")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    inn = message.text

    if inn.isdigit() and len(inn)==10 or len(inn)==12:
        info = get_info_org(inn)
        if info == False:
            bot.send_message(message.from_user.id, "Не удалось получить ответа от сервера.")
        else:
            bot.send_message(message.from_user.id, info["suggestions"][0]["value"] +
                "\nКПП: {}".format(info["suggestions"][0]["data"]["kpp"]) +
                "\nОКАТО: {}".format(info["suggestions"][0]["data"]["okato"]) +
                "\nОКТМО: {}".format(info["suggestions"][0]["data"]["oktmo"]) +
                "\n{}".format(info["suggestions"][0]["data"]["management"]["post"] + ": " + info["suggestions"][0]["data"]["management"]["name"]) +
                "\nАдрес: {}".format(info["suggestions"][0]["data"]["address"]["unrestricted_value"])
                )
        markup_inline = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')

        markup_inline.add(item_yes, item_no)
        bot.send_message(message.chat.id, "Вас интересует данная организация?", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'yes':
                bot.send_message(call.message.chat.id, '😎')
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, '😟')

                #Исчезновение сообщения
                #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="AAA",reply_markup=None)

                #Уведомление
                #bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
    except Exception as e:
        print(repr(e))


def get_info_org(inn):
    headers_auth = {'Authorization': 'Token ' + TOKEN, 'Content-Type': 'application/json'}
    auth = requests.post(URL, headers=headers_auth)

    if auth.status_code == 200:
        params = {
            'query': inn,
            'branch_type': "MAIN"
        }
        r = requests.get(URL, headers=headers_auth, params=params)
        res = r.json()
        return res
    else:
        return False

bot.polling(none_stop=True, interval=0)