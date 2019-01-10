from telegram import Message, Update, Bot, User
from telegram.ext import Filters, MessageHandler, run_async
from googletrans import Translator
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot import dispatcher
@run_async
def translate(bot: Bot, update: Update):
  message = update.effective_message
  text = message.reply_to_message.text
  translator=Translator()
  reply_text=translator.translate(text, dest='en').text
  reply_text="`Source: `\n"+text+"`Translation: `\n"+reply_text
  message.reply_to_message.reply_text(reply_text)
translate_handler = DisableAbleCommandHandler("translate", translate)
dispatcher.add_handler(translate_handler)
