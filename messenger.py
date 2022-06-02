from flask import Flask, request, render_template
from datetime import datetime
import json

application = Flask(__name__)  # Созданием Flask-приложение
DB_FILE = "./data/db.json"  # Путь к файлу DB


def load_messages():
    """Функция чтения сообщений из файла"""

    json_file = open(DB_FILE, "r")
    data = json.load(json_file)  # Чтение данных из файла
    return data["messages"]


all_messages = load_messages()  # Список всех сообщений


def save_messages():
    """Функция для сохранения сообщений в файл"""

    data = {
        "messages": all_messages
    }
    json_file = open(DB_FILE, "w")
    json.dump(data, json_file)  # Записать данные в файл
    pass


@application.route("/chat")
def display_chat():
    return render_template("form.html")


@application.route("/")
def index_page():
    return "Hello, welcome!"


@application.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


@application.route("/send_message")
def send_message():
    sender = request.args["name"]
    text = request.args["text"]
    add_message(sender, text)
    save_messages()
    return "ok"


def add_message(sender, text):
    if 100 > len(sender) > 1 and 1 < len(text) < 3000:
        new_message = {
            "sender": sender,
            "text": text,
            "time": datetime.now().strftime("%H:%M:%S")
        }
        all_messages.append(new_message)


application.run(host='0.0.0.0', port=80)  # Запуск приложения
