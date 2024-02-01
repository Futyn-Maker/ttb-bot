from datetime import datetime
import pytz
from typing import Dict, Optional, Tuple, Union

from bot import db

from responses.history_responses import HISTORY_RESPONSES


moscow_tz = pytz.timezone("Europe/Moscow")

async def generate_history(user: Dict[str, Union[int, str]]) -> Tuple[Optional[str]]:
    if user["name"]:
        name = f"{user['name']} @{user['tg_name']}"
    else:
        name = f"@{user['tg_name']}"

    history = {}
    async for response in db.get_user_responses(user["id"]):
        timestamp_start = datetime.fromisoformat(response["timestamp_start"]).astimezone(moscow_tz)
        date_str = timestamp_start.strftime("%d.%m.%Y")
        time_start_str = timestamp_start.strftime("%H:%M")
        timestamp_end = datetime.fromisoformat(response["timestamp_end"]).astimezone(moscow_tz) if response["timestamp_end"] else None
        time_end_str = timestamp_end.strftime("%H:%M") if timestamp_end else None
        time_entry = f"{time_start_str}-{time_end_str}" if time_end_str else time_start_str
        history_response = HISTORY_RESPONSES["history_response"].format(time=time_entry, text=response["text"])

        if date_str not in history:
            history[date_str] = []
        history[date_str].append(history_response)

    if history:
        history_text = "\n".join([HISTORY_RESPONSES["history_entry"].format(date=date, responses="\n".join(messages)) for date, messages in history.items()])
        return name, history_text
    else:
        return name, HISTORY_RESPONSES["history_empty"]
