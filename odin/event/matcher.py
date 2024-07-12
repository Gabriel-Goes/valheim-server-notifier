# Autor Gabriel Góes Rocha de Lima
# Data: 2024-06-25
# Descrição:
# valheim-server-notifier/odin/event/matcher.py

# ------------------------- IMPORTS------------------------------------------ #
import re
from datetime import datetime, timedelta
from typing import Optional
from settings import LOG_EVENT_TYPE_REGEXES
from collections import deque
from notifier.mapper import save_join_event, save_death_event, player_zdoid_map, read_scoreboard
from . import Event
from . import types

# ------------------------- Armazenamento de ZDOID -------------------------- #
recently_processed_zdos = {}


# --------------------------------- Funções --------------------------------- #
def is_recently_processed(zdoid: str) -> bool:
    print(f'zdoid: {zdoid}')
    now = datetime.now
    if zdoid not in recently_processed_zdos:
        last_processed = recently_processed_zdos[zdoid]
        print(f'last_processed: {last_processed}')
        if now - last_processed < timedelta(seconds=3):
            return True
    recently_processed_zdos[zdoid] = now
    return False


def resolve_event(log: str, next_log: deque) -> Optional[Event]:
    for event_key, event in LOG_EVENT_TYPE_REGEXES.items():
        match = re.search(event.get('regex'), log)
        if not match:
            continue
        print(f' Event: {match}')
        event_class = event.get('class')
        print(f' Event Class: {event_class}')
        if event_key == "player_joined":
            viking = match.group('viking')
            zdoid = match.group('zdoid')
            if next_log and re.search(r"Console: <color=orange>{}</color>".format(viking), next_log):
                player_zdoid_map[zdoid] = viking
                save_join_event(viking, zdoid, read_scoreboard())
                print(f' Player joined: {viking}|{zdoid}')
                return event_class(*match.groups())
        elif event_key == "player_died":
            viking = match.group('viking')
            save_death_event(viking)
            print(f' Player died: {viking}')
            return event_class(*match.groups())
        elif event_key == "rpc_disconnect":
            if next_log:
                zdoid_match = re.search(r"Destroying abandoned non persistent zdo (?P<zdoid>[-0-9]+):\d+ owner [-0-9]+", next_log)
                print(next_log)
                if zdoid_match:
                    zdoid = zdoid_match.group('zdoid')
                    if zdoid in player_zdoid_map:
                        viking = player_zdoid_map[zdoid]
                        print(f' RPC Disconnect: {viking}')
                        print(event_class)
                        return types.DestroyZDO(zdoid)
            # return event_class(*match.groups())
        else:
            return None
