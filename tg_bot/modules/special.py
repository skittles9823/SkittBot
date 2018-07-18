from io import BytesIO
from time import sleep
from typing import Optional, List
from telegram import TelegramError, Chat, Message
from telegram import Update, Bot, User
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown
from tg_bot.modules.helper_funcs.chat_status import is_user_ban_protected, user_admin

import random
import telegram
import tg_bot.modules.sql.users_sql as sql
from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, LOGGER
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.disable import DisableAbleCommandHandler

USERS_GROUP = 4

MESSAGES = (
    "Happy birthday ",
    "Heppi burfdey ",
    "Hep burf ",
    "Happy day of birthing ",
    "Sadn't deathn't-day ",
    "Oof, you were born today ",
)

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
def getlink(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = int(args[0])
    else:
        update.effective_message.reply_text("You don't seem to be referring to a chat")
    try:
        chat = bot.getChat(chat_id)
        bot_member = chat.get_member(bot.id)
        if bot_member.can_invite_users:
            invitelink = bot.exportChatInviteLink(chat_id)
            update.effective_message.reply_text(invitelink)
        else:
            update.effective_message.reply_text("I don't have access to the invite link.")
    except BadRequest as excp:
            update.effective_message.reply_text(excp.message + " " + str(chat_id))

@run_async
def sudolist(bot: Bot, update: Update):
    text = "My sudo users are:"
    for user_id in SUDO_USERS:
        user = bot.get_chat(user_id)
        name = "[{}](tg://user?id={})".format(user.first_name + (user.last_name or ""), user.id)
        if user.username:
            name = escape_markdown("@" + user.username)
        text += "\n - {}".format(name)

    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

@run_async
@user_admin
def birthday(bot: Bot, update: Update, args: List[str]):
    if args:
        username = str(",".join(args))
    for i in range(5):
        bdaymessage = random.choice(MESSAGES)
        update.effective_message.reply_text(bdaymessage + username)

    __help__ = """
*Owner only:*
- /getlink *chatid*: Get the invite link for a specific chat.

*Sudo only:*
- /quickscope *chatid* *userid*: Ban user from chat.
- /quickunban *chatid* *userid*: Unban user from chat.
- /snipe *chatid* *string*: Make me send a message to a specific chat.

*Admin only:*
- /birthday *@username*: Spam user with birthday wishes.
"""

__mod_name__ = "Special"

SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args=True, filters=CustomFilters.sudo_filter)
QUICKSCOPE_HANDLER = CommandHandler("quickscope", quickscope, pass_args=True, filters=CustomFilters.sudo_filter)
QUICKUNBAN_HANDLER = CommandHandler("quickunban", quickunban, pass_args=True, filters=CustomFilters.sudo_filter)
GETLINK_HANDLER = CommandHandler("getlink", getlink, pass_args=True, filters=Filters.user(OWNER_ID))
SLIST_HANDLER = CommandHandler("sudolist", sudolist, filters=Filters.user(OWNER_ID))
BIRTHDAY_HANDLER = CommandHandler("birthday", birthday, pass_args=True, filters=Filters.group)

dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(QUICKSCOPE_HANDLER)
dispatcher.add_handler(QUICKUNBAN_HANDLER)
dispatcher.add_handler(GETLINK_HANDLER)
dispatcher.add_handler(SLIST_HANDLER)
dispatcher.add_handler(BIRTHDAY_HANDLER)
