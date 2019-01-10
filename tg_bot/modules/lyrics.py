from PyLyrics import *
from telegram import Update, Bot
from telegram.ext import run_async
from typing import Optional, List

from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot import dispatcher

from requests import get

LYRICSINFO = "\n[Full Lyrics](https://www.azlyrics.com/lyrics/%s/%s.html)"

@run_async
def lyrics(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    text = message.text[len('/lyrics '):]
    song = " ".join(args).split("- ")
    reply_text = f'Looks up for lyrics'
    
    if len(song) == 2:
        while song[1].startswith(" "):
            song[1] = song[1][1:]
        while song[0].startswith(" "):
            song[0] = song[0][1:]
        while song[1].endswith(" "):
            song[1] = song[1][:-1]
        while song[0].endswith(" "):
            song[0] = song[0][:-1]
        try:
            lyrics = "\n".join(PyLyrics.getLyrics(
                song[0], song[1]).split("\n")[:20])
        except ValueError as e:
            return update.effective_message.reply_text("Song %s not found :(" % song[1], failed=True)
        else:
           
            lyricstext = LYRICSINFO % (song[0].replace(
                " ", ""), song[1].replace(" ", ""))
            return update.effective_message.reply_text(lyrics + lyricstext.lower(), parse_mode="MARKDOWN")
    else:
        return update.effective_message.reply_text("Invalid syntax - try Artist - Title! \n Example : Imagine Dragons - Machine", failed=True)


__help__ = """
 - /lyrics <keyword> Find your favourite songs' lyrics
"""

__mod_name__ = "Lyrics"

LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True)

dispatcher.add_handler(LYRICS_HANDLER)
