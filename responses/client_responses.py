CLIENT_RESPONSES = {
    "start": """
Спасибо, что согласились поучаствовать в исследовании!

Бот будет напоминать несколько раз в день о том, что нужно заполнять дневник, предлагая несколько вариантов ответа (вы всегда можете ввести свой вариант).
Вы можете заполнять дневник:
- в течение дня в реальном времени, отправляя сообщения боту при каждой смене деятельности (в этом случае не нужно указывать время, бот сам его зафиксирует)
- несколько раз за день (например, в 13.00 записать дневник за период времени 8-13, затем в 18 за период 13-18 и т.д.)
- в конце дня одним сообщением, ориентируясь на свои контрольные точки

Пример: 
08.00 подготовка к уроку
09.00 1 урок, проверка самостоятельной 
10.00-10.20 планерка у завуча 
...
15.00-16.00 подготовка проекта 
23.00-00.00 проверка впр 

Нас интересует распределение времени на те или иные виды деятельности в течение рабочего дня, а также работа в нерабочее время. По всем вопросам пишите @annavaskevich
    """,
    "help": """
Бот сохранит текстовое сообщение, которое Вы ему отправите
/ask - бот задаст вопрос и покажет клавиатуру с быстрыми вариантами ответов
/history - бот покажет сохраненные сообщения за весь период
    """,
    "ask": "Что Вы сейчас делаете?",
    "message_saved": "Сообщение сохранено 👍",

}
