# This example show how to use inline keyboards and process button presses
import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, sys
from PIL import Image, ImageDraw, ImageFont
import random

TELEGRAM_TOKEN = '1425859530:AAF5MQE87Zg_bv3B2RLe3Vl2A5rMz6vYpsA'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

channelId = -1001390673326
user_dict = {}


def TextToImg(ext):
    IMAGES = [
        'tmp/AROQ.jpg',
        'tmp/AK47.jpg',
        'tmp/BAXT.jpg',
        'tmp/BASKETBOL.jpg',
        'tmp/BAXTLI.jpg',
        'tmp/DOST.jpg',
        'tmp/ER.jpg',
        'tmp/ETIK.jpg',
        'tmp/FUTBOL.jpg',
        'tmp/GAZ.jpg',
        'tmp/HOTIN.jpg',
        'tmp/BAXT.jpg',
        'tmp/IPHONE.jpg',
        'tmp/KOLBASA.jpg',
        'tmp/KONFET.jpg',
        'tmp/KOZGU.jpg',
        'tmp/KUCHUK.jpg',
        'tmp/MOSHINA.jpg',
        'tmp/NEWISHTON.jpg',
        'tmp/NOTEBOOK.jpg',
        'tmp/OMAD.jpg',
        'tmp/OYINCHOQ.jpg',
        'tmp/PAYPQO.jpg',
        'tmp/BAXT.jpg',
        'tmp/PUL.jpg',
        'tmp/PULTUG.jpg',
        'tmp/QORQIZ.jpg',
        'tmp/SOSISKA.jpg',
        'tmp/TELEFON.jpg',
        'tmp/TELEFONZ.jpg',
        'tmp/TOK.jpg',
        'tmp/TORSHIM.jpg',
        'tmp/TUYA.jpg',
        'tmp/UY.jpg',
        'tmp/ZAMBARAK.jpg'
        
    ]
    try:
        img = random.choice(IMAGES)
    except:
        time.sleep(2)
        img = random.choice(IMAGES)
    # get an image
    base = Image.open(img).convert("RGBA")
    ext = ext.upper()
    text = ext
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", base.size, (255,255,255,0))
    # get a font
    fnt = ImageFont.truetype("OpenSans-Italic.ttf", 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text(((800)/2,(1136)/2), text, font=fnt, fill=(255,0,0,255), anchor='mb')

    out = Image.alpha_composite(base, txt)
    
    filename = random.randint(1,35)
    g = out.save(f'tmp/{filename}.png')
    return filename

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Azo bo'ling", callback_data="cb_yes", url='t.me/onideal'),
                               InlineKeyboardButton("Tasdiqlash", callback_data="cb_no"))
    return markup

def getUserFromChannel(userId):
    u = bot.get_chat_member(channelId, userId)
    return u.status

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        u = getUserFromChannel(call.from_user.id)
        if u == 'member':
            msg = bot.send_message(call.from_user.id, """\
            Juda soz!!!, Ismingizni yozing
            """)
            bot.register_next_step_handler(msg, process_name_step)
        else:
            bot.send_message(call.from_user.id, f"Salom {call.from_user.first_name}, kanallarga a'zo bo'ling va A'zolikni tekshirish buyrug'ini tanlang", reply_markup=gen_markup())

def process_name_step(message):
    try:
        name = message.text
        myfile = TextToImg(name)
        photoSend = open(f'tmp/{myfile}.png', 'rb')
        caption = f'{name} : ismiga sovga @onideal \n@giftmerobot \n@mygiftrobot'
        bot.send_photo(message.chat.id, photoSend, caption=caption)
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    us = getUserFromChannel(message.chat.id)

    if us == 'member':
        msg = bot.send_message(message.chat.id, """\
                Juda soz!!!, Ismingizni yozing
                """)
        bot.register_next_step_handler(msg, process_name_step)
    else:
        bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}, kanallarga a'zo bo'ling va A'zolikni tekshirish buyrug'ini tanlang", reply_markup=gen_markup())


bot.polling(none_stop=True)
