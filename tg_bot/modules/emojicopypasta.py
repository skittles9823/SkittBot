import telegram, random
from telegram import Update, Bot
from telegram.ext import run_async

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler

# D A N K module by @deletescape - based on https://github.com/wrxck/mattata/blob/master/plugins/copypasta.mattata

@run_async
def copypasta(bot: Bot, update: Update):
    message = update.effective_message
    emojis = ["😂", "😂", "👌", "✌", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴", "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩"]
    reply_text = random.choice(emojis)
    for c in message.reply_to_message.text:
        if c == " ":
            reply_text += random.choice(emojis)
        elif c in emojis:
            reply_text += c
            reply_text += random.choice(emojis)
        else:
            if bool(random.getrandbits(1)):
                reply_text += c.upper()
            else:
                reply_text += c.lower()
    reply_text += random.choice(emojis)
    message.reply_to_message.reply_text(reply_text)


__help__ = "/copypasta - Riddles the replied-to message with cancerous emoji. Alias: /😂."
__mod_name__ = "CoPY😂pASTa💦😂👓"


COPYPASTA_HANDLER = DisableAbleCommandHandler("copypasta", copypasta)
COPYPASTA_ALIAS_HANDLER = DisableAbleCommandHandler("😂", copypasta)

dispatcher.add_handler(COPYPASTA_HANDLER)
dispatcher.add_handler(COPYPASTA_ALIAS_HANDLER)
