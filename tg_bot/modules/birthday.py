from datetime  import date
from typing import Optional, List

from telegram import Message, Update, Bot, User, Chat
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html

import tg_bot.modules.sql.birthdays_sql as sql
from tg_bot import dispatcher, SUDO_USERS, SUPPORT_USERS
from tg_bot.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.sql.users_sql import get_all_chats

@run_async
def addbirthday(bot: Bot, update: Update, args: List[int]):
	message = update.effective_message  # type: Optional[Message]
	user_id, month, day = extract_user_and_text(message, args)

	if not user_id:
		message.reply_text("You don't seem to be referring to a user.")
		return

	if not month:
		message.reply_text("You must supply a month.")
		return

	if not day:
		message.reply_text("you must supply a day.")
		return

	user_chat = bot.get_chat(user_id)
	sql.add_birthday(user_id, user_chat.username or user_chat.first_name, month, day)

	message.reply_text("Birthday added. 🎂🎉")

@run_async
def delbirthday(bot: Bot, update: Update, args: List[str]):
	message = update.effective_message  # type: Optional[Message]

	user_id = extract_user(message, args)
	if not user_id:
		message.reply_text("You don't seem to be referring to a user.")
		return

	user_chat = bot.get_chat(user_id)
	if user_chat.type != 'private':
		message.reply_text("That's not a user!")
		return

	if not sql.is_user_birthday(user_id):
		message.reply_text("This user is not in the birthday db!")
		return

	message.reply_text("I'll remove {}\'s birthday.".format(user_chat.first_name))

	sql.del_birthday(user_id)

	message.reply_text("Birthday removed.")

def getbirthday(update, user_id):
	if sql.is_user_birthday(user_id):
		tday = date.today()
		year = 2018
		month = month
		day = day
		bday = date(year, month, day)
		if tday == bday:
			chats = get_all_chats()
			for chat in chats:
				chat_id = chat.chat_id

				# Check if this group has disabled gbans
				if not sql.does_chat_gban(chat_id):
					continue

				try:
					member = chat.get_member(user_id)
				except BadRequest as excp:
					if excp.message == "User not found":
						return ""
					else:
						raise
				if member:
					message("Todays date is " + str(tday) + " " + "UTC, happy birthday {}",
							mention_html(member.user.id, member.user.first_name))

@run_async
def user_check(bot: Bot, update: Update):
	if sql.does_chat_birthday(update.effective_chat.id):
		user = update.effective_user  # type: Optional[User]
		chat = update.effective_chat  # type: Optional[Chat]
		msg = update.effective_message  # type: Optional[Message]

		if user(chat, user.id):
			getbirthday(update, user.id)

		if msg.new_chat_members:
			new_members = update.effective_message.new_chat_members
			for mem in new_members:
				getbirthday(update, mem.id)

		if msg.reply_to_message:
			user = msg.reply_to_message.from_user  # type: Optional[User]
			if user(chat, user.id):
				getbirthday(update, user.id, should_message=False)

@run_async
@user_admin
def bdaystat(bot: Bot, update: Update, args: List[str]):
	if len(args) > 0:
		if args[0].lower() in ["on", "yes"]:
			sql.enable_birthdays(update.effective_chat.id)
			update.effective_message.reply_text("I've enabled birthday notifications in this group. :D "
												"To have your birthday notified to users ask a support or sudo member.")
		elif args[0].lower() in ["off", "no"]:
			sql.disable_birthdays(update.effective_chat.id)
			update.effective_message.reply_text("I've disabled birthday notifications in this group D: "
												"Ya'll are party poopers!")
	else:
		update.effective_message.reply_text("Give me some arguments to choose a setting! on/off, yes/no!\n\n"
											"Your current setting is: {}\n"
											"When True, if it's a users birthday, I'll post a message announcing it. "
											"When False, I'll be sad as this group is full of party poopers "
											";_;".format(sql.does_chat_birthday(update.effective_chat.id)))

def __migrate__(old_chat_id, new_chat_id):
	sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
	return "This chat is celebrating birthdays: `{}`.".format(sql.does_chat_birthday(chat_id))

__help__ = """
*Admin only:*
 - /bdaystat <on/off/yes/no>: Will enable/disable birthday notifications in your group, or return your current settings.

As we all know, us Telegram regulars love to celebrate birthdays, so I decided to give everyone a notification when it's \
a users birthday . They can be enabled for you group by calling \
/bdaystat

*Support/Sudo only:*
 - /addbirthday <user_id, month, day>: To add a users birthday. \
 (Note: the month must be a single digit unless the month is Oct, Nov, or Dec). \
 - /delbirthday <user_id>: To remove a users birthday.
"""

__mod_name__ = "Birthdays"

ADDBDAY_HANDLER = CommandHandler("addbirthday", addbirthday, pass_args=True,
								filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
DELBDAY_HANDLER = CommandHandler("delbirthday", delbirthday, pass_args=True,
								filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
BDAY_STATUS = CommandHandler("bdaystat", bdaystat, pass_args=True, filters=Filters.group)
BDAY_CHECK = MessageHandler(Filters.all & Filters.group, user_check)

dispatcher.add_handler(ADDBDAY_HANDLER)
dispatcher.add_handler(DELBDAY_HANDLER)
dispatcher.add_handler(BDAY_STATUS)
dispatcher.add_handler(USER_CHECK)
