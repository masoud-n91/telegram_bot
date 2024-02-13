import telebot
from telebot import types
import os
from openai import OpenAI
import json


os.environ['OPENAI_API_KEY'] = "<openai key>"
os.environ['OPENAI_API_MODEL'] = 'gpt-3.5-turbo-1106'


my_keyboard = types.ReplyKeyboardMarkup(row_width=3)
key0 = types.KeyboardButton("/start")
key1 = types.KeyboardButton("/scientist")
key2 = types.KeyboardButton("/lover")
key3 = types.KeyboardButton("/angry")
key4 = types.KeyboardButton("/heart_broken")
key5 = types.KeyboardButton("/hafez")
my_keyboard.add(key0, key1, key2, key3, key4, key5)


bot = telebot.TeleBot("<TOKEN>", parse_mode=None) 


@bot.message_handler(commands=['start'])
def prompt_scientist(message):
	global prompt, client, history
	text = "welcome to this chatbot. Select your mood and start chating in English. ENJOY!!!"
	bot.send_message(message.chat.id, text, reply_markup=my_keyboard)
	client = OpenAI()
	client.api_key  = os.environ['OPENAI_API_KEY']
	prompt = "You are a chatbot designed to output JSON with key as 'response'. Please give a proper response to the following message!"
	history = []


@bot.message_handler(commands=['scientist'])
def prompt_scientist(message):
	global prompt, history
	history = []
	prompt = "You are a scientist designed to output JSON with key as 'response'. Please reply the following message in the most scientific way!"
	bot.send_message(message.chat.id, "Now you can start chatting!", reply_markup=my_keyboard)
	

@bot.message_handler(commands=['hafez'])
def prompt_scientist(message):
	global prompt, history
	history = []
	prompt = "You are a chatbot representing Hafez, the most famous poet of Persia, designed to output JSON with key as 'response'. Please reply the following message in the best way possible!"
	bot.send_message(message.chat.id, "Now you can start chatting!", reply_markup=my_keyboard)
	

@bot.message_handler(commands=['lover'])
def prompt_lover(message):
	global prompt, history
	history = []
	prompt = "You are a lover designed to output JSON with key as 'response'. Please reply the following message in a romantic way!"
	bot.send_message(message.chat.id, "Now you can start chatting!", reply_markup=my_keyboard)
	

@bot.message_handler(commands=['angry'])
def prompt_angry(message):
	global prompt, history
	history = []
	prompt = "You are an angry chatbot designed to output JSON with key as 'response'. please response to the following message in an angry way"
	bot.send_message(message.chat.id, "Now you can start chatting!", reply_markup=my_keyboard)
	

@bot.message_handler(commands=['heart_broken'])
def prompt_heartBroken(message):
	global prompt, history
	history = []
	prompt = "You are a heart broken chatbot designed to output JSON with key as 'response'. pelase give a sad response to the following message"
	bot.send_message(message.chat.id, "Now you can start chatting!", reply_markup=my_keyboard)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	global prompt, history, client
	prompt = prompt
	chat_history = "\n\n".join(history)
	message_and_history = "Chat history:{" + chat_history + "\n}" + "Message:\n\n{" + message.text + "\n}"
	response = client.chat.completions.create(
		model="gpt-3.5-turbo-1106",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message_and_history}
        ]
        )
	response = response.choices[0].message.content
	json_response = json.loads(response)
	bot_response = json_response.get("response", "Please say it again!")
	if len(history) >= 5:
		history.pop(0)
	history.append(f"\n\nUser_message: {message.text}\nBot_reply: {bot_response}")

	bot.send_message(message.chat.id, bot_response, reply_markup=my_keyboard)
        


bot.infinity_polling()

