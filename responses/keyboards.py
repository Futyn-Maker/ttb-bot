from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Buttons for ask_keyboard
_button_lesson = KeyboardButton("🔍 Урок")
_button_preparation = KeyboardButton("😎 Подготовка")
_button_journal = KeyboardButton("☸ Журнал")
_button_work_with_kids = KeyboardButton("📞 Работа с детьми")
_button_parents = KeyboardButton("📢 Родители")
_button_meeting = KeyboardButton("⭐️ Совещание")
_button_check_work = KeyboardButton("👥 Проверка работ")

ASK_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
ASK_KEYBOARD.add(_button_lesson, _button_preparation)
ASK_KEYBOARD.add(_button_journal, _button_work_with_kids)
ASK_KEYBOARD.add(_button_parents, _button_meeting, _button_check_work)


# Keyboards for registration form

_gender_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Мужской"),
    KeyboardButton("Женский")
)

_class_management_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Да"),
    KeyboardButton("Нет")
)

_consent_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("✅ Даю согласие"),
)

FORM_KEYBOARDS = {
    "gender": _gender_keyboard,
    "class_management": _class_management_keyboard,
    "consent_study": _consent_keyboard,
    "consent_personal_data": _consent_keyboard
}
