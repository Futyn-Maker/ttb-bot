from aiogram import types
from aiogram_forms import fields, forms, validators

from bot import db

from responses.client_responses import CLIENT_RESPONSES
from responses.keyboards import ASK_KEYBOARD, FORM_KEYBOARDS


class RegistrationForm(forms.Form):
    name: str = "RegistrationForm"

    age = fields.StringField("Укажите Ваш возраст (только число)", validators=[validators.RegexValidator(r"^\d+$")], validation_error_message="Неправильный формат ввода. Введите, пожалуйста, только число.")
    gender = fields.ChoicesField("Ваш пол", ["Мужской", "Женский"], reply_keyboard=FORM_KEYBOARDS["gender"], validation_error_message="Неправильный формат ввода. Пожалуйста, выберите: \"Мужской\" или \"Женский\".")
    workplace = fields.StringField("Укажите Ваше место работы")
    workload = fields.StringField("Укажите Вашу нагрузку (сколько часов в неделю)", validators=[validators.RegexValidator(r"^\d+$")], validation_error_message="Неправильный формат ввода. Введите, пожалуйста, только число.")
    subjects = fields.StringField("Какой предмет/предметы Вы ведете?")
    teaching_experience = fields.StringField("Ваш педагогический стаж? (лет)", validators=[validators.RegexValidator(r"^\d+$")], validation_error_message="Неправильный формат ввода. Введите, пожалуйста, только число.")
    class_management = fields.ChoicesField("Есть ли у Вас классное руководство?", ["Да", "Нет"], reply_keyboard=FORM_KEYBOARDS["class_management"], validation_error_message="Неправильный формат ввода. Пожалуйста, выберите: \"Да\" или \"Нет\".")
    classes = fields.StringField("В каких классах Вы преподаете? Укажите параллели через запятую")
    consent_study = fields.ChoicesField("Согласие на участие в исследовании. Мы просим Вас дать согласие на Ваше участие в мониторинговом исследовании, а также других исследованиях, проводимых НИУ ВШЭ, в том числе на использование в научных целях данных из Вашего дневника времени при условии дальнейшего обезличивания данных для защиты прав на неприкосновенность частной жизни, личную и семейную тайну.", ["✅ Даю согласие"], reply_keyboard=FORM_KEYBOARDS["consent_study"], validation_error_message="Для продолжения необходимо дать согласие.")
    consent_personal_data = fields.ChoicesField("Согласие на обработку персональных данных. В соответствии с Федеральным законом от 27.07.2006 № 152-ФЗ «О персональных данных» настоящим даю согласие на обработку моих персональных данных/персональных данных представляемого лица, включая сбор, запись, систематизацию, накопление, хранение, уточнение (обновление, изменение), извлечение, использование, передачу (распространение, предоставление, доступ), обезличивание, блокирование, удаление, уничтожение персональных данных. Согласие дается на сбор и обработку персональных данных в образовательных целях, а также в исследовательских целях в исследованиях, осуществляемых НИУ ВШЭ, при условии дальнейшего обезличивания данных для защиты прав на неприкосновенность частной жизни, личную и семейную тайну. Согласие дается свободно, своей воле и в своем интересе/в интересе представляемого лица. Согласие распространяется на следующие персональные данные: фамилия, имя и отчество субъекта персональных данных; год, месяц, дата и место рождения субъекта персональных данных; наименование образовательной организации (место работы субъекта персональных данных); а также любая иная информация, относящаяся к личности субъекта персональных данных, собранная в ходе исследований НИУ ВШЭ. Содержание действий по обработке персональных данных, необходимость их выполнения, а также мои права по отзыву данного согласия мне понятны. Настоящее согласие действует со дня его подписания и до дня отзыва в письменной форме.", ["✅ Даю согласие"], reply_keyboard=FORM_KEYBOARDS["consent_personal_data"], validation_error_message="Для продолжения необходимо дать согласие.")


async def on_form_finished():
    form_data = await RegistrationForm.get_data()
    message = types.Message.get_current()
    tg_id = message.from_user.id
    tg_name = message.from_user.username
    first_name, last_name = message.from_user.first_name, message.from_user.last_name
    name = f"{first_name} {last_name}" if first_name and last_name else first_name if first_name else None

    age = form_data.get("RegistrationForm:age")
    gender = form_data.get("RegistrationForm:gender")
    workplace = form_data.get("RegistrationForm:workplace")
    workload = form_data.get("RegistrationForm:workload")
    subjects = form_data.get("RegistrationForm:subjects")
    teaching_experience = form_data.get("RegistrationForm:teaching_experience")
    class_management = form_data.get("RegistrationForm:class_management") == "Да"
    classes = form_data.get("RegistrationForm:classes")
    consent_study = form_data.get("RegistrationForm:consent_study") == "✅ Даю согласие"
    consent_personal_data = form_data.get("RegistrationForm:consent_personal_data") == "✅ Даю согласие"
    await db.add_user(tg_id=tg_id, tg_name=tg_name, name=name, age=age, gender=gender, workplace=workplace, workload=workload, subjects=subjects, teaching_experience=teaching_experience, class_management=class_management, classes=classes, consent_study=consent_study, consent_personal_data=consent_personal_data)
    await message.answer(text=CLIENT_RESPONSES["start"], reply_markup=ASK_KEYBOARD)
