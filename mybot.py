import telebot
import sqlite3
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup

bot = telebot.TeleBot('8862117918:AAHmZrBNyHH7nmM25lt4N6LWWxp-wwRtVdo')

connection = sqlite3.connect('users.db')
cursor = connection.cursor()
create_table_query ="""
    CREATE TABLE IF NOT EXISTS users(
        id integer primary key,
        first_name text,
        last_name text,
        phone_number text
    );
"""
cursor.execute(create_table_query)
connection.commit()
connection.close()


fetch_data_query = """
    SELECT id, first_name, last_name, phone_number FROM users
"""
rows = []

with sqlite3.connect('users.db') as connection:
    cursor = connection.cursor()
    cursor.execute(fetch_data_query)
    rows = cursor.fetchall()

for row in rows:
    print(f'ID:{row[0]}, FN:{row[1]}, LN:{row[2]}, PN:{row[3]}')




user_ID = []

reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
reply_keyboard.add('buy', 'exit')
#-----------------------------------
button1 = InlineKeyboardButton(text="youtube", url="https://www.youtube.com")
button2 = InlineKeyboardButton(text="google", url="https://www.google.com")
button3 = InlineKeyboardButton(text="button3", callback_data="btn3")

inline_keyboard = InlineKeyboardMarkup(row_width=2)
inline_keyboard.add(button1, button2, button3)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "welcome to microlearn Bot.", reply_markup=inline_keyboard)


#-----------------------------------


@bot.message_handler(commands=['SUPU2024'])
def send_update(message):
    for id in user_ID:
        bot.send_message(id, "The product is available.")

@bot.callback_query_handler(func=lambda call:True)
def check_button(call):
	if call.data == "btn3":
		bot.answer_callback_query(call.id, "Btn3 is tapped.", show_alert=True)


#-----------------------------------

        
@bot.message_handler(commands=['pay']) 
def welcome(message): 
	bot.reply_to(message,"Check the following keyboard.", reply_markup=reply_keyboard)

@bot.message_handler(func=lambda message: True)
def check_button(message):
	if message.text == 'buy':
		bot.reply_to(message, "button1 is pressed.")
	elif message.text == 'exit':
		bot.reply_to(message, 'button2 is pressed.')
	else:
		bot.reply_to(message, f'Your message is: {message.text}')
		

bot.polling()