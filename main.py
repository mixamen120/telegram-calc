import telebot
import math
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(token="6753365422:AAFyeVKBU_4-lMQjvMWgoBMuza2apRTeN18")
numbers = '0123456789'

@bot.message_handler(commands=["start"])
def welcome(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Привет!")

@bot.message_handler(commands=["how_are_you"])
def how_are_you(message: Message):
    keyboard = ReplyKeyboardMarkup()
    button1 = KeyboardButton(text="Хорошо")
    button2 = KeyboardButton(text="Плохо")
    keyboard.add(button1, button2)
    msg = bot.send_message(chat_id=message.chat.id, text="Хорошо, а у тебя?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, define_answer_for_how_are_you)

def define_answer_for_how_are_you(message: Message):
    if message.text.lower() == "хорошо":
        bot.send_message(chat_id=message.chat.id, text="Супер!")
    elif message.text.lower() == "плохо":
        bot.send_message(chat_id=message.chat.id, text="Не супер")
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю")


@bot.message_handler(commands=["calculate"])
def calculate(message: Message):
    keyboard = ReplyKeyboardMarkup()
    button1 = KeyboardButton(text="+")
    button2 = KeyboardButton(text="-")
    button3 = KeyboardButton(text="%")
    button4 = KeyboardButton(text="/")
    button5 = KeyboardButton(text="*")
    button6 = KeyboardButton(text="^")
    button7 = KeyboardButton(text="√")
    button8 = KeyboardButton(text="sin")
    button9 = KeyboardButton(text="cos")
    button10 = KeyboardButton(text="tan")
    button11 = KeyboardButton(text="| |")
    keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10)
    msg = bot.send_message(chat_id=message.chat.id, text="Выберите операцию.", reply_markup=keyboard)
    bot.register_next_step_handler(msg, define_number1)


def define_number1(message: Message):
    operation = message.text
    msg = bot.send_message(chat_id=message.chat.id, text="Введите первое число")
    if operation in ['√', 'sin', 'cos', 'tan', '| |']:
        bot.register_next_step_handler(msg, one_number_calculator, operation)
    else:
        bot.register_next_step_handler(msg, define_number2, operation)

def define_number2(message: Message, operation):
    if message.text.isdigit():
        num1 = int(message.text)
    else:
        bot.send_message(chat_id=message.chat.id, text="Вы ввели не число, попробуйте еще раз запустить команду")
        return
    msg = bot.send_message(chat_id=message.chat.id, text="Введите второе число")
    bot.register_next_step_handler(msg, calculator, operation, num1)

def calculator(message: Message, operation, num1):
    if message.text.isdigit():
        num2 = int(message.text)
    else:
        bot.send_message(chat_id=message.chat.id, text="Вы ввели не число, попробуйте еще раз запустить команду")
        return
    #operations = {"+", "-", "*", "/", "%", "^"}
    result = 0

    if operation == "+":
        result = int(num1)+int(num2)
    elif operation == "-":
        result = int(num1)-int(num2)
    elif operation == "*":
        result = int(num1)*int(num2)
    elif operation == "/":
        result = int(num1)/int(num2)
    elif operation == "%":
        result = int(num1)%int(num2)
    elif operation == "^":
        result = int(num1)**int(num2)

    bot.send_message(chat_id=message.chat.id, text=f"{result} - результат")

def one_number_calculator(message: Message, operation):
    result = 0
    num1 = int(message.text)

    if operation == '√':
        if num1 >= 0:
            result = math.sqrt(int(num1))
        else:
            msg = bot.send_message(chat_id=message.chat.id, text="Число отрицательное - нельзя вычислить корень!")
    elif operation == 'sin':
        result = math.sin(int(num1))
    elif operation == 'cos':
        result = math.cos(int(num1))
    elif operation == 'tan':
        result = math.tan(int(num1))
    elif operation == '| |':
        result = abs(int(num1))

    bot.send_message(chat_id=message.chat.id, text=f"{result} - результат")

bot.polling()