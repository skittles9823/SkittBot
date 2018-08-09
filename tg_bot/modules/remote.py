from tg_bot.modules.notes import get
from telegram.ext import CommandHandler
from tg_bot import dispatcher
from tg_bot.modules.sql.remote_sql import connect, disconnect, get_connected_chat

def connect_chat(bot, update, args):
    if len(args) >= 1 and update.effective_chat.type == 'private':
        try:
            connect_chat = int(args[0])
        except ValueError:
            update.effective_message.reply_text("Invalid Chat ID provided!")
        if bot.get_chat_member(connect_chat, update.effective_message.from_user.id).status in ('administrator', 'creator', 'member'):
            connection_status = connect(update.effective_message.from_user.id, connect_chat)
            print(bot.get_chat_member(connect_chat, update.effective_message.from_user.id))
            if connection_status:
                update.effective_message.reply_text(f"Successfully connected to {connect_chat}!")
            else:
                update.effective_message.reply_text("Connection failed!")
        else:
            update.effective_message.reply_text("You are not a participant of the given chat, Go away!")

    elif len(args) >=1 and not update.effective_chat.type == 'private':
        update.effective_message.reply_text("Usage limited to PMs only!")
    elif update.effective_chat.type == 'private' and not len(args) >= 1:
        update.effective_message.reply_text("Gimme a chat to connect to!")
    else:
        update.effective_message.reply_text("Duh, gimme a chat and do it in your PMs")

def disconnect_chat(bot, update):
    if update.effective_chat.type == 'private':
        disconnection_status = disconnect(update.effective_message.from_user.id)
        if disconnection_status:
           disconnected_chat = update.effective_message.reply_text("Disconnected from chat!")
        else:
           update.effective_message.reply_text("Disconnection unsuccessfull!")
    else:
        update.effective_message.reply_text("Usage restricted to PMs only")

CONNECT_CHAT_HANDLER = CommandHandler("connect", connect_chat, allow_edited=True, pass_args=True)
DISCONNECT_CHAT_HANDLER = CommandHandler("disconnect", disconnect_chat, allow_edited=True)

dispatcher.add_handler(CONNECT_CHAT_HANDLER)
dispatcher.add_handler(DISCONNECT_CHAT_HANDLER)
