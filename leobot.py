import json
import requests
import time
import urllib.parse

TOKEN = "499561911:AAFHaBMl67ieOSjjZ0MDYdOEMby-NJahp1g"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
materias = ["Sistemas de Informação", "Compiladores", "Banco de Dados II", "Redes I", "MDS II"]
link_prova = "https://drive.google.com/file/d/1nHl346achwzY4_2cf9ZX7t4-bL_XTgIh/view?usp=sharing"


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            username = update["message"]["chat"]["username"]
            if text.startswith("/"):
                #items = db.get_items(chat)
                if text == "/start":
                    #keyboard = build_keyboard(items)
                    send_message("Olá "+username+" serei seu parceiro na sua jornada durante o curso de SI da UNEB. atualmente posso lhe ajudar com esses comandos: ", chat)
                    send_message("*/prova:* Lista as provas antigas da matéria a ser selecionada.\n */prova nome_da_materia:* Lista as provas antigas das matérias com o nome passado.", chat, "Markdown")
                elif text == "/help":
                    send_message("Olá "+username+", atualmente posso lhe ajudar com esses comandos: ", chat)
                    send_message("*/prova:* Lista as provas antigas da matéria a ser selecionada.\n */prova nome_da_materia:* Lista as provas antigas desta matéria.", chat, "Markdown")
                elif text.startswith("/prova"):
                    school_theme = text.split("/prova", 1)[1]
                    if school_theme == "":
                        send_message("[Compila 2016.1]("+link_prova+")\n[Banco de Dados]("+link_prova+")", chat, "Markdown")
                    else:
                        send_message("[Compila 2017.2]("+link_prova+")", chat, "Markdown")
        except KeyError:
            pass

def get_last_chat_info(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    text.encode('utf-8')
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    print("Received: "+text)
    text1 = urllib.parse.quote_plus(text)
    #print("Must send: " + text1)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    if reply_markup == "Markdown":
        url += "&parse_mode={}".format("Markdown")
    elif reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def build_keyboard(items):
    '''keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)'''

def main():
    last_update_id = None
    while True:
        print("Waiting messages...")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)

if __name__ == '__main__':
    main()
