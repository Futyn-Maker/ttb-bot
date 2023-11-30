from datetime import datetime
import pytz
from typing import Dict, Optional, Tuple, Union

from bot import db

from responses.client_responses import CLIENT_RESPONSES

moscow_tz = pytz.timezone("Europe/Moscow")

async def generate_history(user: Dict[str, Union[int, str]]) -> Tuple[Optional[str]]:
    if user["name"]:
        name = f"{user['name']} @{user['tg_name']}"
    else:
        name = f"@{user['tg_name']}"

    history = {}
    async for response in db.get_user_responses(user["id"]):
        timestamp = datetime.fromisoformat(response["timestamp"]).astimezone(moscow_tz)
        date_str = timestamp.strftime("%d.%m.%Y")
        time_str = timestamp.strftime("%H:%M")
        history_response = CLIENT_RESPONSES["history_response"].format(time=time_str, text=response["text"])

        if date_str not in history:
            history[date_str] = []
        history[date_str].append(history_response)

    if history:
        history_text = "\n".join([CLIENT_RESPONSES["history_entry"].format(date=date, responses="\n".join(messages)) for date, messages in history.items()])
        return name, history_text
    else:
        return name, CLIENT_RESPONSES["history_empty"]
