import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('Your key')

notes = {}

@bot.message_handler(commands=['start'])
def main(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("add")
    markup.row(btn1)
    btn2 = KeyboardButton("list")
    btn3 = KeyboardButton("clear")
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Привет", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "add":
        bot.send_message(message.chat.id, 'type your note')
        bot.register_next_step_handler(message, save_note)

    elif message.text == "list":
        show_notes(message)
        bot.register_next_step_handler(message, on_click)

    elif message.text == "clear":
        notes[message.chat.id] = []
        bot.send_message(message.chat.id, 'Notes cleared')
        bot.register_next_step_handler(message, on_click)

def save_note(message):
    chat_id = message.chat.id

    if chat_id not in notes:
        notes[chat_id] = []

    notes[chat_id].append(message.text)
    bot.send_message(chat_id, "Note added")
    bot.register_next_step_handler(message, on_click)

def show_notes(message):
    chat_id = message.chat.id

    if chat_id not in notes or not notes[chat_id]:
        bot.send_message(chat_id, "No notes yet")
        return

    text = "Your notes:\n"
    for i, note in enumerate(notes[chat_id], 1):
        text += f"{i}. {note}\n"

    bot.send_message(chat_id, text)

@bot.message_handler()
def info(message):
    bot.reply_to(message, "start again!")

bot.infinity_polling()