from io import BytesIO
from time import sleep
from typing import Optional

from telegram import TelegramError, Chat, Message
from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async

import tg_bot.modules.sql.users_sql as sql
import tg_bot.modules.sql.global_bans_sql as gban_sql
from tg_bot import dispatcher, SUDO_USERS, SUPPORT_USERS, OWNER_ID, LOGGER
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.helper_funcs.misc import send_to_list
from tg_bot.modules.sql.users_sql import get_all_chats

import requests

USERS_GROUP = 4


def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith('@'):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = dispatcher.bot.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message == 'Chat not found':
                    pass
                else:
                    LOGGER.exception("Error extracting user ID")

    return None


@run_async
def broadcast(bot: Bot, update: Update):
    to_send = update.effective_message.text.split(None, 1)
    if len(to_send) >= 2:
        chats = sql.get_all_chats() or []
        failed = 0
        for chat in chats:
            try:
                bot.sendMessage(int(chat.chat_id), to_send[1])
                sleep(0.1)
            except TelegramError:
                failed += 1
                LOGGER.warning("Couldn't send broadcast to %s, group name %s", str(chat.chat_id), str(chat.chat_name))

        update.effective_message.reply_text("Broadcast complete. {} groups failed to receive the message, probably "
                                            "due to being kicked.".format(failed))


@run_async
def log_user(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    id = msg.from_user.id
    username = msg.from_user.username
    sql.update_user(id,
                    username,
                    chat.id,
                    chat.title)
    __check_cas__(bot, id, username)

    if msg.reply_to_message:
        id = msg.reply_to_message.from_user.id
        username = msg.reply_to_message.from_user.username
        sql.update_user(id,
                        username,
                        chat.id,
                        chat.title)
        __check_cas__(bot, id, username)

    if msg.forward_from:
        id = msg.forward_from.id
        username = msg.forward_from.username
        sql.update_user(id, username)
        __check_cas__(bot, id, username)
        


@run_async
def chats(bot: Bot, update: Update):
    all_chats = sql.get_all_chats() or []
    chatfile = 'List of chats.\n'
    for chat in all_chats:
        chatfile += "{} - ({})\n".format(chat.chat_name, chat.chat_id)

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        update.effective_message.reply_document(document=output, filename="chatlist.txt",
                                                caption="Here is the list of chats in my database.")


def __user_info__(user_id):
    if user_id == dispatcher.bot.id:
        return """I've seen them in... Wow. Are they stalking me? They're in all the same places I am... oh. It's me."""
    num_chats = sql.get_user_num_chats(user_id)
    return """I've seen them in <code>{}</code> chats in total.""".format(num_chats)


def __stats__():
    return "{} users, across {} chats".format(sql.num_users(), sql.num_chats())


def __gdpr__(user_id):
    sql.del_user(user_id)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)

CAS_URL = "https://combot.org/api/cas/check"

def __check_cas__(bot: Bot, user_id, username):
    json = requests.get(CAS_URL, params={"user_id": str(user_id)}).json()
    cas_banned = json["ok"] and (json["result"] and json["result"]["offenses"] > 0)
    if cas_banned:
        reason = f"User is CAS-Banned (https://combot.org/cas/query?u={user_id})"
        send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
            "<b>Global Ban</b>" \
            "\n#GBAN, #AUTO, #CAS" \
            "\n<b>Status:</b> <code>Enforcing</code>" \
            "\n<b>Sudo Admin:</b> <code>Automated Ban</code>" \
            "\n<b>User:</b> {}" \
            "\n<b>ID:</b> <code>{}</code>" \
            "\n<b>Reason:</b> {}".format(mention_html(user_id, username), 
                user_id, reason), html=True)
        gban_sql.gban_user(user_id, username or user_chat, reason)
        chats = get_all_chats()
        for chat in chats:
            chat_id = chat.chat_id

            # Check if this group has disabled gbans
            if not gban_sql.does_chat_gban(chat_id):
                continue

            try:
                bot.kick_chat_member(chat_id, user_id)
            except BadRequest as excp:
                if excp.message in GBAN_ERRORS:
                    pass
                else:
                    send_to_list(bot, SUDO_USERS + SUPPORT_USERS, "Could not gban due to: {}".format(excp.message))
                    gban_sql.ungban_user(user_id)
                    return
            except TelegramError:
                pass
        send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                "{} has been successfully gbanned!".format(mention_html(user_id, username)), html=True)

__help__ = ""  # no help string

__mod_name__ = "Users"

BROADCAST_HANDLER = CommandHandler("broadcast", broadcast, filters=Filters.user(OWNER_ID))
USER_HANDLER = MessageHandler(Filters.all & Filters.group, log_user)
CHATLIST_HANDLER = CommandHandler("chatlist", chats, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
dispatcher.add_handler(BROADCAST_HANDLER)
dispatcher.add_handler(CHATLIST_HANDLER)
