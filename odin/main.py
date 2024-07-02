# Autor Gabriel Góes Rocha de Lima
# Data: 2024-06-25
# Descrição: Script principal para monitoramento de logs do Valheim
# valheim-server-notifier/odin/main.py
# Última atualização: 2024-06-29
# Versão: 0.1.1
# --------------------------------------------------------------------------- #
# Este projeto é um fork do projeto:
#    https://github.com/jaumebecks/valheim-server-notifier

# ------------------------- IMPORTS------------------------------------------ #
from lib.config import VALHEIM_LOG_PATH, DISCORD_WEBHOOK_URL, SCOREBOARD_FILE
from lib.utils import read_logs
from event.matcher import resolve_event
from notifier.mapper import build_template
from notifier.discord import publish_event
from collections import deque


# --------------------------- MAIN ------------------------------------------ #
def main():
    if VALHEIM_LOG_PATH is None:
        raise EnvironmentError('Missing <VALHEIM_LOG_PATH> envvar')

    if DISCORD_WEBHOOK_URL is None:
        raise EnvironmentError('Missing <DISCORD_WEBHOOK_URL> envvar')

    if SCOREBOARD_FILE is None:
        raise EnvironmentError('Missing <SCOREBOARD_FILE> envvar')

    logs = read_logs(path=VALHEIM_LOG_PATH)
    previous_logs = deque(maxlen=2)

    for log in logs:
        if log:
            event = resolve_event(log, previous_logs)
            if event:
                print(f'Event: {event}')
                template = build_template(event)
                publish_event(DISCORD_WEBHOOK_URL, template)
        previous_logs.append(log)


# -------------------------- EXECUÇÃO --------------------------------------- #
if __name__ == '__main__':
    main()
