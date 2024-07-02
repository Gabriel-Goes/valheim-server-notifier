import re
from typing import Optional
from settings import LOG_EVENT_TYPE_REGEXES
from collections import deque
from notifier.mapper import save_join_event, save_death_event, player_zdoid_map, read_scoreboard
from . import Event


def resolve_event(log: str, previous_logs: deque) -> Optional[Event]:
    print(log)
    for event_key, event in LOG_EVENT_TYPE_REGEXES.items():
        match = re.search(event.get('regex'), log)
        if not match:
            continue

        event_class = event.get('class')
        print(f"Matched event: {event_class.__name__}")

        if event_key == "player_joined":
            viking = match.group('viking')
            zdoid = match.group('zdoid')
            player_zdoid_map[zdoid] = viking
            save_join_event(viking, zdoid, read_scoreboard())
        elif event_key == "player_died":
            viking = match.group('viking')
            save_death_event(viking)
        elif event_key == "rpc_disconnect":
            previous_logs.append(log)
            return None
        elif event_key == "destriy_zdo" and previous_logs and "RPC_Disconnect" in previous_logs[-1]:
            zdoid = match.group('zdoid')
            viking = player_zdoid_map.pop(zdoid, 'Unknown')
            print(f"Player {viking}|({zdoid}) disconnected")
            previous_logs.clear()
            return event_class(zdoid, viking)
        return event_class(*match.groups())

    return None
