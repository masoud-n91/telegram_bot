import telebot
from telebot import types
import os
import random
from jdatetime import date
from gtts import gTTS
import qrcode


main_keyboard = types.ReplyKeyboardMarkup(row_width=3)
key1 = types.KeyboardButton("/game")
key2 = types.KeyboardButton("/age")
key3 = types.KeyboardButton("/voice")
key4 = types.KeyboardButton("/max")
key5 = types.KeyboardButton("/argmax")
key6 = types.KeyboardButton("/qrcode")
key7 = types.KeyboardButton("/help")
main_keyboard.add(key1, key2, key3, key4, key5, key6, key7)

game_keyboard = types.ReplyKeyboardMarkup(row_width=3)
gkey1 = types.KeyboardButton("/new_game")
gkey2 = types.KeyboardButton("/return_to_main_menu")
game_keyboard.add(gkey1, gkey2)


bot = telebot.TeleBot("<TOKEN>", parse_mode=None) 


@bot.message_handler(commands=['help'])
def start_menu(message):
	text = """command /start: print welcome with user name (e.g. Hello Sajjad, Welcome to this bot).
	\ncommand /game: Run the guessing number game. The user guesses a number and the bot guides (go up, go down, you win) - while playing, a new game button should be seen at the bottom.
	\ncommand /age: Get the date of birth in Hijri and calculate the age. (Hint: Checkout @pylearn page in Instagram).
	\ncommand /voice: Get a sentence in English from the user and convert it to voice.
	\ncommand /max: Receive an array from the user and print the largest value. numbers should seperate with comma, e.g. 14,7,78,15,8,19,20.
	\ncommand /argmax: Get an array from the user and print the index of the largest value.
	\ncommand /qrcode: Get a string from the user and generate its qrcode."""
	bot.send_message(message.chat.id, text, reply_markup=main_keyboard)
	

@bot.message_handler(commands=['start'])
def start_menu(message):
	global stat
	stat = ""
	bot.send_message(message.chat.id, "Hello Sajjad, Welcome to this bot", reply_markup=main_keyboard)
	

@bot.message_handler(commands=['return_to_main_menu'])
def restart_menu(message):
	global stat
	stat = ""
	bot.send_message(message.chat.id, "Choose an option from the menu.", reply_markup=main_keyboard)
	

@bot.message_handler(commands=['game'])
def create_game(message):
	global random_number, stat
	stat = "game"
	random_number = random.randint(0, 999)
	bot.send_message(message.chat.id, "Now you can start guessing a number between 0 to 999!\n Have fun", reply_markup=game_keyboard)
	

@bot.message_handler(commands=['new_game'])
def recreate_game(message):
	global random_number, stat
	stat = "game"
	random_number = random.randint(0, 999)
	bot.send_message(message.chat.id, "Guess another number between 0 to 999!\n Have fun", reply_markup=game_keyboard)
	

@bot.message_handler(commands=['age'])
def cal_age(message):
	global stat
	stat = "age"
	bot.send_message(message.chat.id, "Enter your birthdate. e.g. 26/01/1370", reply_markup=main_keyboard)
	

@bot.message_handler(commands=['voice'])
def gen_tts(message):
	global stat
	stat = "voice"
	bot.send_message(message.chat.id, "Type something in English", reply_markup=main_keyboard)
	

@bot.message_handler(commands=['max'])
def find_max(message):
	global stat
	stat = "max"
	bot.send_message(message.chat.id, "Enter a list of numbers. Numbers should seperate with comma, e.g. 14,7,78,15,8,19,20", reply_markup=main_keyboard)


@bot.message_handler(commands=['argmax'])
def find_max_idx(message):
	global stat
	stat = "argmax"
	bot.send_message(message.chat.id, "Enter a list of numbers. Numbers should seperate with comma, e.g. 14,7,78,15,8,19,20", reply_markup=main_keyboard)


@bot.message_handler(commands=['qrcode'])
def prompt_lover(message):
	global stat
	stat = "qrcode"
	bot.send_message(message.chat.id, "Write something!", reply_markup=main_keyboard)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	global random_number, stat
	if stat == "game":
		try:
			if int(message.text) > random_number:
				bot.send_message(message.chat.id, "Go down", reply_markup=game_keyboard)
			elif int(message.text) < random_number:
				bot.send_message(message.chat.id, "Go up", reply_markup=game_keyboard)
			elif int(message.text) == random_number:
				bot.send_message(message.chat.id, "Hoooooraaay. You guessed right.", reply_markup=game_keyboard)
				recreate_game(message)
		except:
			bot.send_message(message.chat.id, "Give a number not a word", reply_markup=game_keyboard)
	if stat == "age":
		try:
			day, month, year = message.text.split("/")
			birthdate = date(int(year), int(month), int(day))
			age = calculate_age(birthdate)
			bot.send_message(message.chat.id, f"You are {age} years old", reply_markup=main_keyboard)
		except:
			bot.send_message(message.chat.id, "Please enter a correct format of your birthdate!", reply_markup=main_keyboard)
	if stat == "voice":
		try:
			text_to_speech(message.text)
			voice = open('output.mp3', 'rb')
			bot.send_voice(message.chat.id, voice)
		except:
			bot.send_message(message.chat.id, "Oooops!", reply_markup=main_keyboard)
	if stat == "max":
		try:
			numbers = message.text.split(",")
			int_numbers = list(map(int, numbers))
			max_num = max(int_numbers)
			bot.send_message(message.chat.id, f"The maximum is {max_num}", reply_markup=main_keyboard)
		except:
			bot.send_message(message.chat.id, "Pay attention to the format!!!", reply_markup=main_keyboard)
	if stat == "argmax":
		try:
			numbers = message.text.split(",")
			int_numbers = list(map(int, numbers))
			max_num = max(int_numbers)
			arg_max_num = int_numbers.index(max_num)
			bot.send_message(message.chat.id, f"The index of maximum number is {arg_max_num}", reply_markup=main_keyboard)
		except:
			bot.send_message(message.chat.id, "Pay attention to the format!!!", reply_markup=main_keyboard)
	if stat == "qrcode":
		try:
			qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
			qr.add_data(message.text)
			qr.make(fit=True)
			img = qr.make_image(fill_color="black", back_color="white")
			img.save("qr_code.png")
			photo = open('qr_code.png', 'rb')
			bot.send_photo(message.chat.id, photo)
		except:
			bot.send_message(message.chat.id, "Ooooppps!!!", reply_markup=main_keyboard)
			
		
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
	
def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


bot.infinity_polling()

