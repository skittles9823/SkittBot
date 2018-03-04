from io import BytesIO
from time import sleep
from typing import Optional, List
from telegram import TelegramError, Chat, Message
from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async
from tg_bot.modules.helper_funcs.chat_status import is_user_ban_protected

import telegram, random
import tg_bot.modules.sql.users_sql as sql
from tg_bot import dispatcher, OWNER_ID, LOGGER
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.disable import DisableAbleCommandHandler

USERS_GROUP=4
                                                                                                                                                                                                                                                                               
@run_async                                                                                                                                                                                                                                                                     
def quickscope(bot: Bot, update: Update, args: List[int]):                                                                                                                                                                                                                     
    if args:                                                                                                                                                                                                                                                                   
        chat_id = str(args[1])                                                                                                                                                                                                                                                 
        to_kick = str(args[0])                                                                                                                                                                                                                                                 
    else:                                                                                                                                                                                                                                                                      
        update.effective_message.reply_text("You don't seem to be referring to a chat/user")                                                                                                                                                                                   
    try:                                                                                                                                                                                                                                                                       
        bot.kick_chat_member(chat_id, to_kick)                                                                                                                                                                                                                                 
        update.effective_message.reply_text("Attempted banning " + to_kick + " from" + chat_id)                                                                                                                                                                                
    except BadRequest as excp:                                                                                                                                                                                                                                                 
        update.effective_message.reply_text(excp.message + " " + to_kick)                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                               
@run_async                                                                                                                                                                                                                                                                     
def quickunban(bot: Bot, update: Update, args: List[int]):                                                                                                                                                                                                                     
    if args:                                                                                                                                                                                                                                                                   
        chat_id = str(args[1])                                                                                                                                                                                                                                                 
        to_kick = str(args[0])                                                                                                                                                                                                                                                 
    else:                                                                                                                                                                                                                                                                      
        update.effective_message.reply_text("You don't seem to be referring to a chat/user")                                                                                                                                                                                   
    try:                                                                                                                                                                                                                                                                       
        bot.unban_chat_member(chat_id, to_kick)                                                                                                                                                                                                                                
        update.effective_message.reply_text("Attempted unbanning " + to_kick + " from" + chat_id)
    except BadRequest as excp:
        update.effective_message.reply_text(excp.message + " " + to_kick)

@run_async
def banall(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = str(args[0])
        all_mems = sql.get_chat_members(chat_id)
    else:
        chat_id = str(update.effective_chat.id)
        all_mems = sql.get_chat_members(chat_id)
    for mems in all_mems:
        try:
            bot.kick_chat_member(chat_id, mems.user)
            update.effective_message.reply_text("Tried banning " + str(mems.user))
            sleep(0.1)
        except BadRequest as excp:
            update.effective_message.reply_text(excp.message + " " + str(mems.user))
            continue


@run_async
def snipe(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError as excp:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text("Couldn't send the message. Perhaps I'm not part of that group?")

@run_async
def chats(bot: Bot, update: Update):
    chats = sql.get_all_chats() or []

    chatfile = 'List of chats.\n'
    for chat in chats:
        chatfile += "[x] {} - {}\n".format(chat.chat_name, chat.chat_id)

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        update.effective_message.reply_document(document=output, filename="chatlist.txt",
                                                caption="Here is the list of chats in my database.")

# D A N K module by @deletescape - based on https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata

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
	
# D A N K module by @deletescape 

@run_async
def bmoji(bot: Bot, update: Update):
    message = update.effective_message
    b_char = random.choice(message.reply_to_message.text).lower() # choose a random character in the message to be substituted with 🅱️
    reply_text = message.replace(b_char, "🅱️").replace(b_char.upper(), "🅱️")
    message.reply_to_message.reply_text(reply_text)

@run_async
def clapmoji(bot: Bot, update: Update):
    message = update.effective_message
    reply_text = "👏 "
    for i in message.reply_to_message.text:
        if i == " ":
            reply_text += " 👏 "
        else:
            reply_text += i
    reply_text += " 👏"
    message.reply_to_message.reply_text(reply_text)

__help__ = ""  # no help string

__mod_name__ = "Special"

CHATSS_HANDLER = CommandHandler("chats", chats, filters=CustomFilters.sudo_filter)
SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args = True, filters=CustomFilters.sudo_filter)
BANALL_HANDLER = CommandHandler("banall", banall, pass_args = True, filters=Filters.user(OWNER_ID))
QUICKSCOPE_HANDLER = CommandHandler("quickscope", quickscope, pass_args = True, filters=CustomFilters.sudo_filter)
QUICKUNBAN_HANDLER = CommandHandler("quickunban", quickunban, pass_args = True, filters=CustomFilters.sudo_filter)
COPYPASTA_HANDLER = DisableAbleCommandHandler("copypasta", copypasta)
COPYPASTA_ALIAS_HANDLER = DisableAbleCommandHandler("😂", copypasta)
CLAPMOJI_HANDLER = DisableAbleCommandHandler("clapmoji", clapmoji)
CLAPMOJI_ALIAS_HANDLER = DisableAbleCommandHandler("👏", clapmoji)
BMOJI_HANDLER = DisableAbleCommandHandler("🅱️", bmoji)

dispatcher.add_handler(CHATSS_HANDLER)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(BANALL_HANDLER)
dispatcher.add_handler(QUICKSCOPE_HANDLER)
dispatcher.add_handler(QUICKUNBAN_HANDLER)
dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(COPYPASTA_ALIAS_HANDLER)
dispatcher.add_handler(CLAPMOJI_HANDLER)
dispatcher.add_handler(CLAPMOJI_ALIAS_HANDLER)
dispatcher.add_handler(BMOJI_HANDLER)
