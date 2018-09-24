import random, re, string, io, asyncio
from PIL import Image
from io import BytesIO
from spongemock import spongemock
from zalgo_text import zalgo
from deeppyer import deepfry
import os
from pathlib import Path
import shutil
import ast
import numpy

import nltk # shitty lib, but it does work
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from typing import Optional, List
from telegram import Message, Update, Bot, User, Chat
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async

from tg_bot import dispatcher, DEEPFRY_TOKEN
from tg_bot.modules.disable import DisableAbleCommandHandler

WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
WIDE_MAP[0x20] = 0x3000

# D A N K modules by @deletescape vvv

# based on https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata
@run_async
def copypasta(bot: Bot, update: Update):
    message = update.effective_message
    emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
    reply_text = random.choice(emojis)
    b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
    for c in message.reply_to_message.text:
        if c == " ":
            reply_text += random.choice(emojis)
        elif c in emojis:
            reply_text += c
            reply_text += random.choice(emojis)
        elif c.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(random.getrandbits(1)):
                reply_text += c.upper()
            else:
                reply_text += c.lower()
    reply_text += random.choice(emojis)
    message.reply_to_message.reply_text(reply_text)


@run_async
def bmoji(bot: Bot, update: Update):
    message = update.effective_message
    b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
    reply_text = message.reply_to_message.text.replace(b_char, "🅱️").replace(b_char.upper(), "🅱️")
    message.reply_to_message.reply_text(reply_text)


@run_async
def clapmoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "👏 "
    reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
    reply_text += " 👏"
    message.reply_to_message.reply_text(reply_text)


@run_async
def owo(bot: Bot, update: Update):
    message = update.effective_message
    faces = ['(・`ω´・)',';;w;;','owo','UwU','>w<','^w^','\(^o\) (/o^)/','( ^ _ ^)∠☆','(ô_ô)','~:o',';____;', '(*^*)', '(>_', '(♥_♥)', '*(^O^)*', '((+_+))']
    reply_text = re.sub(r'[rl]', "w", message.reply_to_message.text)
    reply_text = re.sub(r'[ｒｌ]', "ｗ", message.reply_to_message.text)
    reply_text = re.sub(r'[RL]', 'W', reply_text)
    reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
    reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
    reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
    reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
    reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
    reply_text = re.sub(r'\!+', ' ' + random.choice(faces), reply_text)
    reply_text = re.sub(r'！+', ' ' + random.choice(faces), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
    reply_text += ' ' + random.choice(faces)
    message.reply_to_message.reply_text(reply_text)


@run_async
def stretch(bot: Bot, update: Update):
    message = update.effective_message
    count = random.randint(3, 10)
    reply_text = re.sub(r'([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])', (r'\1' * count), message.reply_to_message.text)
    message.reply_to_message.reply_text(reply_text)


@run_async
def vapor(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if not message.reply_to_message:
        if not args:
            message.reply_text("I need a message to convert to vaporwave text.")
        else:
            noreply = True
            data = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        noreply = False
        data = message.reply_to_message.text
    else:
        data = ''

    reply_text = str(data).translate(WIDE_MAP)
    if noreply:
        message.reply_text(reply_text)
    else:
        message.reply_to_message.reply_text(reply_text)

# D A N K modules by @deletescape ^^^
# Less D A N K modules by @skittles9823 # holi fugg I did some maymays vvv

@run_async
def spongemocktext(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = ''

    reply_text = spongemock.mock(data)
    message.reply_to_message.reply_text(reply_text)


@run_async
def zalgotext(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = ''

    z = zalgo.zalgo()
    reply_text = z.zalgofy(data)
    message.reply_to_message.reply_text(reply_text)

# Less D A N K modules by @skittles9823 # holi fugg I did some maymays ^^^
# shitty maymay modules made by @divadsn vvv

@run_async
def forbesify(bot: Bot, update: Update):
    message = update.effective_message
    if message.reply_to_message:
        data = message.reply_to_message.text
    else:
        data = ''

    data = data.lower()
    accidentals = ['VB', 'VBD', 'VBG', 'VBN']
    reply_text = data.split()
    offset = 0

    # use NLTK to find out where verbs are
    tagged = dict(nltk.pos_tag(reply_text))

    # let's go through every word and check if it's a verb
    # if yes, insert ACCIDENTALLY and increase offset
    for k in range(len(reply_text)):
        i = reply_text[k + offset]
        if tagged.get(i) in accidentals:
            reply_text.insert(k + offset, 'accidentally')
            offset += 1

    reply_text = string.capwords(' '.join(reply_text))
    message.reply_to_message.reply_text(reply_text)


deepdata = []
deepdata2 = []
deepdata3 = []
imgno = 0
chat_id = []
fps = 0.0

@run_async
def deepfryer(bot: Bot, update: Update):
    global deepdata
    global deepdata2
    global deepdata3
    message = update.effective_message
    if message.reply_to_message:
        deepdata = message.reply_to_message.photo
        deepdata2 = message.reply_to_message.sticker
        deepdata3 = message.reply_to_message.animation
    else:
        deepdata = []
        deepdata2 = []
        deepdata3 = []

    # check if message does contain a photo and cancel when not
    if not deepdata and not deepdata2 and not deepdata3:
        message.reply_text("What am I supposed to do with this?!")
        return

    # download last photo (highres) as byte array
    if deepdata:
        photodata = deepdata[len(deepdata) - 1].get_file().download_as_bytearray()
        image = Image.open(io.BytesIO(photodata))
    elif deepdata2:
        sticker = bot.get_file(deepdata2.file_id)
        sticker.download('sticker.png')
        image = Image.open("sticker.png")
    elif deepdata3:
        global fps
        global imgno
        global chat_id
        chat_id = update.effective_chat.id
        message.reply_text("detected gif")
        gif = bot.get_file(deepdata3.file_id)
        gif.download('gif.mp4')
        if not Path('gifdata').is_dir():
            os.makedirs('gifdata')
        jsondata = ast.literal_eval(os.popen('ffprobe -i gif.mp4 -v quiet -print_format json -show_format -show_streams -hide_banner').read())
        stringfps = jsondata["streams"][0]["avg_frame_rate"]
        templist= []
        for i in stringfps.split('/'):
            templist.append(float(i))
        fps = numpy.divide(templist[0], templist[1])
        os.system('ffmpeg -i gif.mp4 -r {} gifdata/out%05d.jpg'.format(fps)) 
        duration = float(jsondata["streams"][0]["duration"])
        imgno = int(duration*fps)
        image = 0

    # the following needs to be executed async (because dumb lib)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(process_deepfry(image, message.reply_to_message, bot))
    loop.close()

async def process_deepfry(image: Image, reply: Message, bot: Bot):
    # DEEPFRY IT
    if deepdata or deepdata2:
        image = await deepfry(
            img=image,
            token=DEEPFRY_TOKEN,
            url_base='westeurope'
        )

        bio = BytesIO()
        bio.name = 'image.jpeg'
        image.save(bio, 'JPEG')
    
    elif deepdata3:
        for i in range(1, imgno+1):
            if i < 10:
                imagew = Image.open('gifdata/out0000{}.jpg'.format(i))
            elif i >= 10 and i < 100:
                imagew = Image.open('gifdata/out000{}.jpg'.format(i))
            elif i >= 100:
                imagew = Image.open('gifdata/out00{}.jpg'.format(i))
            image = await deepfry(
                    img=imagew,
                    token=None,
                    url_base='westeurope',
                    )
            image.save('./image{}.jpg'.format(i), 'jpeg')
        delay = 100/fps
        os.system('convert -delay {} -loop 0 *.jpg final.gif'.format(delay))
        meh = 'final.gif'

    # send it back
    if deepdata or deepdata2:
        bio.seek(0)
        reply.reply_photo(bio)
    elif deepdata3:
        bot.send_animation(chat_id=chat_id, animation=open('final.gif', 'rb'))
     
    if Path("image1.jpg").is_file():
        for i in range(1, imgno+1):
            os.remove('image{}.jpg'.format(i))
    if Path("sticker.png").is_file():
        os.remove("sticker.png")
    if Path('gifdata').is_dir():
        shutil.rmtree('gifdata')
    if Path('gif.mp4').is_file():
        os.remove("gif.mp4")
    if Path('final.gif').is_file():
        os.remove('final.gif')

# shitty maymay modules made by @divadsn ^^^

# no help string
__help__ = """
 many memz
 Thanks @deletescape and @divadsn for the meme commands :D
"""

__mod_name__ = "Memes"

COPYPASTA_HANDLER = DisableAbleCommandHandler("😂", copypasta)
CLAPMOJI_HANDLER = DisableAbleCommandHandler("👏", clapmoji, admin_ok=True)
BMOJI_HANDLER = DisableAbleCommandHandler("🅱", bmoji, admin_ok=True)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo, admin_ok=True)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor", vapor, pass_args=True, admin_ok=True)
MOCK_HANDLER = DisableAbleCommandHandler("mock", spongemocktext, admin_ok=True)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext)
FORBES_HANDLER = DisableAbleCommandHandler("forbes", forbesify, admin_ok=True)
DEEPFRY_HANDLER = DisableAbleCommandHandler("deepfry", deepfryer, admin_ok=True)

dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
dispatcher.add_handler(FORBES_HANDLER)
dispatcher.add_handler(DEEPFRY_HANDLER)

