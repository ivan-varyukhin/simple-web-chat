from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)

DB_FILE = "data/db.json"


def load_messages():
    with open(DB_FILE, "r") as json_file:
        data = json.load(json_file)
        return data["messages"]


all_messages = load_messages()


def save_messages():
    with open(DB_FILE, "w") as json_file:
        data = {
            "messages": all_messages
        }
        json.dump(data, json_file)


def add_message(text, sender):
    current_time = datetime.now().strftime("%H:%M:%S")
    new_message = {
        "text": text,
        "sender": sender,
        "time": current_time
    }
    all_messages.append(new_message)
    save_messages()


def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['time']}")


def print_all_messages():
    for msg in all_messages:
        print_message(msg)


@app.route("/")
def main_page():
    return "Hello, welcome to SkillChat"


@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


@app.route("/send_message")
def send_message():
    text = request.args["text"]
    sender = request.args["name"]
    add_message(text, sender)
    return "OK"


@app.route("/chat")
def display_chat():
    return render_template("form.html")


app.run()
