import re
from typing import Optional
from settings import LOG_EVENT_TYPE_REGEXES
from notifier.mapper import save_join_event, save_death_event, player_zdoid_map, read_scoreboard
from . import Event


def resolve_event(log: str) -> Optional[Event]:
    print(f' Resolving event: {log}')
    for event_key, event in LOG_EVENT_TYPE_REGEXES.items():
        match = re.search(event.get('regex'), log)
        if not match:
            continue

        event_class = event.get('class')
        if event_key == "player_got_zdoid":
            viking = match.group('viking')
            zdoid = match.group('zdoid')
            player_zdoid_map[zdoid] = viking
            save_join_event(viking, zdoid, read_scoreboard())

        elif event_key == "player_died":
            viking = match.group('viking')
            save_death_event(viking)

        return event_class(*match.groups())

    return None
