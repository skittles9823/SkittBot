import threading

from sqlalchemy import Column, UnicodeText, Integer, String, Boolean

from tg_bot.modules.sql import BASE, SESSION

class Birthdays(BASE):
	__tablename__ = "birthdays"
	user_id = Column(Integer, primary_key=True)
	name = Column(UnicodeText, nullable=False)
	month = Column(Integer)
	day = Column(Integer)

	def __init__(self, user_id, name, month, day):
		self.user_id = user_id
		self.name = name
		self.month = month
		self.day = day

	def __repr__(self):
		return "<Birthday User {} ({})>".format(self.name, self.user_id)

	def to_dict(self):
		return {"user_id": self.user_id,
				"name": self.name,
				"month": self.month,
				"day": self.day}


class BirthdaySettings(BASE):
	__tablename__ = "birthday_settings"
	chat_id = Column(String(14), primary_key=True)
	setting = Column(Boolean, default=False, nullable=False)

	def __init__(self, chat_id, enabled):
		self.chat_id = str(chat_id)
		self.setting = enabled

	def __repr__(self):
		return "<Birthday setting {} ({})>".format(self.chat_id, self.setting)


Birthdays.__table__.create(checkfirst=True)
BirthdaySettings.__table__.create(checkfirst=True)

BIRTHDAY_LOCK = threading.RLock()
BIRTHDAY_SETTING_LOCK = threading.RLock()
BIRTHDAY_LIST = set()
BIRTHDAYSTAT_LIST = set()


def add_birthday(user_id, name, month, day):
	with BIRTHDAY_LOCK:
		user = SESSION.query(Birthdays).get(user_id)
		if not user:
			user = Birthdays(user_id, name, month, day)
		else:
			user.name = name
			user.month = month
			user.day = day

		SESSION.merge(user)
		SESSION.commit()
		__load_birthday_userid_list()


def del_birthday(user_id):
	with BIRTHDAY_LOCK:
		user = SESSION.query(Birthdays).get(user_id)
		if user:
			SESSION.delete(user)

		SESSION.commit()
		__load_birthday_userid_list()


def is_user_birthday(user_id):
	return user_id in BIRTHDAY_LIST


def get_birthday_user(user_id):
	try:
		return SESSION.query(Birthdays).get(user_id)
	finally:
		SESSION.close()


def enable_birthdays(chat_id):
	with BIRTHDAY_LOCK:
		chat = SESSION.query(BirthdaySettings).get(str(chat_id))
		if not chat:
			chat = BirthdaySettings(chat_id, True)

		chat.setting = True
		SESSION.add(chat)
		SESSION.commit()
		if str(chat_id) in BIRTHDAYSTAT_LIST:
			BIRTHDAYSTAT_LIST.remove(str(chat_id))


def disable_birthdays(chat_id):
	with BIRTHDAY_LOCK:
		chat = SESSION.query(BirthdaySettings).get(str(chat_id))
		if not chat:
			chat = BirthdaySettings(chat_id, False)

		chat.setting = False
		SESSION.add(chat)
		SESSION.commit()
		BIRTHDAYSTAT_LIST.add(str(chat_id))


def does_chat_birthday(chat_id):
	return str(chat_id) not in BIRTHDAYSTAT_LIST


def __load_birthday_userid_list():
	global BIRTHDAY_LIST
	try:
		BIRTHDAY_LIST = {x.user_id for x in SESSION.query(Birthdays).all()}
	finally:
		SESSION.close()


def __load_birthday_stat_list():
	global BIRTHDAYSTAT_LIST
	try:
		BIRTHDAYSTAT_LIST = {x.chat_id for x in SESSION.query(BirthdaySettings).all() if not x.setting}
	finally:
		SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
	with BIRTHDAY_LOCK:
		chat = SESSION.query(BirthdaySettings).get(str(old_chat_id))
		if chat:
			chat.chat_id = new_chat_id
			SESSION.add(chat)

		SESSION.commit()


# Create in memory userid to avoid disk access
__load_birthday_userid_list()
__load_birthday_stat_list()
