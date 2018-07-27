import random, re
from spongemock import spongemock
from zalgo_text import zalgo

from typing import Optional, List
from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async

from tg_bot import dispatcher
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
        noreply = True
        data = message.text.split(None, 1)[1]
        if not args:
            message.reply_text("I need a message to convert to vaporwave text.")
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

# no help string
__help__ = """
 many memz
 Thanks @deletescape for the meme commands :D
"""

__mod_name__ = "Memes"

COPYPASTA_HANDLER = DisableAbleCommandHandler("copypasta", copypasta)
COPYPASTA_ALIAS_HANDLER = DisableAbleCommandHandler("😂", copypasta)
CLAPMOJI_HANDLER = DisableAbleCommandHandler("clapmoji", clapmoji)
CLAPMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("👏", clapmoji)
BMOJI_HANDLER = DisableAbleCommandHandler("🅱️", bmoji)
BMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("bmoji", bmoji)
OWO_HANDLER = DisableAbleCommandHandler("owo", owo)
STRETCH_HANDLER = DisableAbleCommandHandler("stretch", stretch)
VAPOR_HANDLER = DisableAbleCommandHandler("vapor", vapor, pass_args=True)
MOCK_HANDLER = DisableAbleCommandHandler("mock", spongemocktext)
ZALGO_HANDLER = DisableAbleCommandHandler("zalgofy", zalgotext)

dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(COPYPASTA_ALIAS_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(CLAPMOJI_ALIAS_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
dispatcher.add_handler(BMOJI_ALIAS_HANDLER)
dispatcher.add_handler(OWO_HANDLER)
dispatcher.add_handler(STRETCH_HANDLER)
dispatcher.add_handler(VAPOR_HANDLER)
dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(ZALGO_HANDLER)
